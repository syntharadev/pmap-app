-- ==============================================================================
-- PMAP.APP - SUPABASE INITIALIZATION: LICENSES
-- Archivo: 001_init_licenses.sql
-- ==============================================================================

-- 1. CREACIÓN DE LA TABLA
CREATE TABLE public.sys_license (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    license_key TEXT UNIQUE NOT NULL,
    email TEXT,
    tier TEXT CHECK (tier IN ('indie', 'pro', 'enterprise')),
    status TEXT CHECK (status IN ('active', 'revoked')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Índices para búsquedas ultra-rápidas por clave (esencial para el arranque del nodo local)
CREATE INDEX idx_sys_license_key ON public.sys_license (license_key);

-- 2. HABILITAR SEGURIDAD RLS
ALTER TABLE public.sys_license ENABLE ROW LEVEL SECURITY;

-- 3. POLÍTICA 2 (NODO CLOUD): Acceso total para service_role (Webhook)
CREATE POLICY "Service Role Full Access" 
ON public.sys_license
FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

-- 4. POLÍTICA 1 (NODO LOCAL): Acceso público
-- NOTA ARQUITECTÓNICA CRÍTICA: PostgreSQL RLS *no puede* inspeccionar la cláusula WHERE 
-- de una consulta SELECT para saber si el usuario pasó un "license_key" exacto.
-- Si ponemos USING (true) para anon, cualquiera podría hacer `select *` y descargar la base de clientes.
--
-- SOLUCIÓN: Deshabilitar el SELECT directo a `anon` y usar una Función Segura (RPC).
-- Esta función actúa como un "agujero de gusano" validado.

CREATE POLICY "Deny direct anon select to prevent scraping" 
ON public.sys_license
FOR SELECT 
TO anon 
USING (false);

-- FUNCIÓN RPC (Stored Procedure) para el cliente Python:
CREATE OR REPLACE FUNCTION verify_license_secure(p_key TEXT)
RETURNS TABLE (tier TEXT, status TEXT)
SECURITY DEFINER -- Se ejecuta con privilegios de bypass temporal
AS $$
BEGIN
  RETURN QUERY SELECT l.tier, l.status FROM public.sys_license l WHERE l.license_key = p_key;
END;
$$ LANGUAGE plpgsql;

-- Permitir a anon ejecutar la función
GRANT EXECUTE ON FUNCTION verify_license_secure(TEXT) TO anon;
