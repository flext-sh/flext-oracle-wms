# flext-oracle-wms - Oracle WMS Integration
PROJECT_NAME := flext-oracle-wms
include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
