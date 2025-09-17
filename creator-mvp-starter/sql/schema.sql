create extension if not exists pgcrypto;

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  password_hash text,
  created_at timestamptz default now()
);

create table if not exists connectors (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  platform text not null,  -- 'youtube' | 'instagram' | 'patreon'
  access_token_enc text not null,
  refresh_token_enc text,
  scopes jsonb,
  consent_ts timestamptz default now()
);

create index if not exists idx_connectors_user on connectors(user_id);

create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  platform text not null,
  platform_post_id text,
  ts timestamptz,
  text text,
  media_type text,
  metrics jsonb
);

create table if not exists metrics_aggregates (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  date date not null,
  platform text not null,
  followers bigint,
  views bigint,
  watch_time bigint,
  est_revenue numeric
);

create table if not exists recommendations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  created_at timestamptz default now(),
  payload jsonb,
  feedback text
);
