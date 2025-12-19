# flext-oracle-wms - Oracle WMS Integration
PROJECT_NAME := flext-oracle-wms
COV_DIR := flext_oracle_wms
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
