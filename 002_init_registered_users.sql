-- ==============================================================================
-- PMAP.APP - SUPABASE INITIALIZATION: REGISTERED USERS (FOSS Gated Model)
-- Archivo: 002_init_registered_users.sql
-- ==============================================================================

-- 1. TRANSFORMACIÓN O CREACIÓN DE LA TABLA
-- Si ya existía sys_license:
-- ALTER TABLE public.sys_license RENAME TO registered_users;
-- ALTER TABLE public.registered_users DROP COLUMN IF EXISTS tier;

CREATE TABLE IF NOT EXISTS public.registered_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Índices para búsquedas ultra-rápidas por correo electrónico
CREATE INDEX IF NOT EXISTS idx_registered_users_email ON public.registered_users (email);

-- 2. HABILITAR SEGURIDAD RLS (Row Level Security)
ALTER TABLE public.registered_users ENABLE ROW LEVEL SECURITY;

-- 3. POLÍTICA DE REGISTRO (FRONTEND SERVERLESS): Permitir inserciones públicas de email
CREATE POLICY "Allow public registration inserts" 
ON public.registered_users
FOR INSERT 
TO anon 
WITH CHECK (true);

-- 4. POLÍTICA DE VALIDACIÓN (NODO LOCAL): Permitir consultas SELECT de emails individuales
-- Permite que el nodo local verifique si un correo específico existe
CREATE POLICY "Allow email verification select" 
ON public.registered_users
FOR SELECT 
TO anon 
USING (true);
