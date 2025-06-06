#!/bin/bash
set -e
psql -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS postgis;"