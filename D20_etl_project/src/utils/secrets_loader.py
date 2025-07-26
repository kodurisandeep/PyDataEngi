from google.cloud import secretmanager

def load_secrets_from_gcp(secret_names, project_id):
    client = secretmanager.SecretManagerServiceClient()
    resolved = {}
    for name in secret_names:
        secret_path = f"projects/{project_id}/secrets/{name}/versions/latest"
        try:
            response = client.access_secret_version(name=secret_path)
            resolved[name] = response.payload.data.decode("UTF-8")
        except Exception as e:
            resolved[name] = None
    return resolved