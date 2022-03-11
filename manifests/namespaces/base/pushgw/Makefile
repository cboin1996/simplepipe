../pushgw.yaml:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo update
	helm template pushgw prometheus-community/prometheus-pushgateway >> ../pushgw.yaml
