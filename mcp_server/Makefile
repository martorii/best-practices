# =======================
# CONFIG
# =======================
IMAGE_NAME      := mcp-server
IMAGE_TAG       := v1.0.0
CONTAINER_NAME  := mcp-server

PORTS := 8000:8000
ENV_VARS :=
VOLUMES :=

# =======================
# COLORS
# =======================
RESET   := \033[0m
BOLD    := \033[1m
GREEN   := \033[32m
CYAN    := \033[36m
YELLOW  := \033[33m
RED     := \033[31m

# =======================
# LOGGING MACROS
# =======================
define log
	@printf "$(CYAN)[%s]$(RESET) $(BOLD)$(1)$(RESET)\n" "$$(date +%H:%M:%S)"
endef

define ok
	@printf "$(GREEN)[✔]$(RESET) %s\n" "$(1)"
endef

define warn
	@printf "$(YELLOW)[!]$(RESET) %s\n" "$(1)"
endef

define err
	@printf "$(RED)[✖]$(RESET) %s\n" "$(1)"
endef

# =======================
# INTERNALS
# =======================
PORT_ARGS := $(foreach p,$(PORTS),-p $(p))
ENV_ARGS  := $(foreach e,$(ENV_VARS),-e $(e))
VOL_ARGS  := $(foreach v,$(VOLUMES),-v $(v))

.PHONY: build run stop rm restart logs shell status

# =======================
# TARGETS
# =======================

build:
	$(call log,Building Docker image $(IMAGE_NAME):$(IMAGE_TAG))
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	$(call ok,Image built)

run: build stop
	$(call log,Starting container $(CONTAINER_NAME))
	docker run -d \
		--name $(CONTAINER_NAME) \
		$(PORT_ARGS) \
		$(ENV_ARGS) \
		$(VOL_ARGS) \
		--restart unless-stopped \
		$(IMAGE_NAME):$(IMAGE_TAG)
	$(call ok,Container is running)
	@echo "Ports: $(PORTS)"

stop:
	$(call warn,Stopping container if it exists)
	-@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	$(call ok,Stopped)

rm: stop
	$(call warn,Removing container if it exists)
	-@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	$(call ok,Removed)

restart: rm run

logs:
	$(call log,Streaming logs)
	docker logs -f $(CONTAINER_NAME)

shell:
	$(call log,Opening shell)
	docker exec -it $(CONTAINER_NAME) /bin/sh

status:
	$(call log,Container status)
	-@docker ps -a --filter name=$(CONTAINER_NAME)
