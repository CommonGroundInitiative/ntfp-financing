-- ============================================================
-- NTFP Schemes — Supabase Schema
-- Paste this entire file into Supabase → SQL Editor → Run
-- ============================================================

-- ── Tables ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS schemes (
  id                        uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  scheme_no                 text,
  name                      text NOT NULL,
  ministry                  text,
  fund_recipient            text,
  socio_economic_preference text DEFAULT 'Open to All',
  state_central             text DEFAULT 'Central',
  status                    text DEFAULT 'pending'
                              CHECK (status IN ('active', 'pending', 'archived')),
  submitted_by              text,          -- name/org of contributor (optional)
  created_at                timestamptz DEFAULT now(),
  updated_at                timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scheme_activities (
  id                  uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  scheme_id           uuid REFERENCES schemes(id) ON DELETE CASCADE NOT NULL,
  end_recipient_type  text,
  value_chain_activity text,
  financing_type      text,
  financing_notes     text,
  link                text
);

-- ── Auto-update updated_at ───────────────────────────────────

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER schemes_updated_at
  BEFORE UPDATE ON schemes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── Row Level Security ───────────────────────────────────────

ALTER TABLE schemes          ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheme_activities ENABLE ROW LEVEL SECURITY;

-- Public: read active schemes only
CREATE POLICY "public_read_active_schemes"
  ON schemes FOR SELECT
  USING (status = 'active');

-- Public: insert new schemes (always lands as pending — enforced below)
CREATE POLICY "public_insert_pending_schemes"
  ON schemes FOR INSERT
  WITH CHECK (status = 'pending');

-- Authenticated admin: read ALL schemes (including pending)
CREATE POLICY "admin_read_all_schemes"
  ON schemes FOR SELECT
  TO authenticated
  USING (true);

-- Authenticated admin: update any scheme (approve / edit / archive)
CREATE POLICY "admin_update_schemes"
  ON schemes FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Authenticated admin: delete any scheme
CREATE POLICY "admin_delete_schemes"
  ON schemes FOR DELETE
  TO authenticated
  USING (true);

-- Public: read activities for active schemes
CREATE POLICY "public_read_active_activities"
  ON scheme_activities FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM schemes
      WHERE schemes.id = scheme_activities.scheme_id
        AND schemes.status = 'active'
    )
  );

-- Authenticated admin: read all activities
CREATE POLICY "admin_read_all_activities"
  ON scheme_activities FOR SELECT
  TO authenticated
  USING (true);

-- Public: insert activities (for contributions)
CREATE POLICY "public_insert_activities"
  ON scheme_activities FOR INSERT
  WITH CHECK (true);

-- Authenticated admin: update / delete activities
CREATE POLICY "admin_update_activities"
  ON scheme_activities FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "admin_delete_activities"
  ON scheme_activities FOR DELETE
  TO authenticated
  USING (true);

-- ── Useful indexes ───────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_schemes_status
  ON schemes(status);

CREATE INDEX IF NOT EXISTS idx_schemes_ministry
  ON schemes(ministry);

CREATE INDEX IF NOT EXISTS idx_schemes_preference
  ON schemes(socio_economic_preference);

CREATE INDEX IF NOT EXISTS idx_activities_scheme_id
  ON scheme_activities(scheme_id);

CREATE INDEX IF NOT EXISTS idx_activities_financing_type
  ON scheme_activities(financing_type);

CREATE INDEX IF NOT EXISTS idx_activities_value_chain
  ON scheme_activities(value_chain_activity);

-- ── Done ─────────────────────────────────────────────────────
-- Next step: go to Supabase → Authentication → Users
-- and create your admin account (any email + password).
-- That account can then log in via the Admin tab in the web app.
