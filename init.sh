#!/bin/bash

# Vérifie si Minikube est déjà en cours d'exécution
if minikube status | grep -q "Running"; then
    echo "Minikube is already running"
    exit 1
fi

# Vérifie si on est dans le bon dossier
pwd=$(pwd)
dirname=$(basename "$pwd")
if [ "$dirname" != "Healthcare-analysis" ]; then
    echo "The script should be launched in the Healthcare-analysis directory"
    exit 1
fi

echo "Downloading CRD ..."
kubectl create -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
echo "Done ..."

echo "Applying config files for K8S ..."
kubectl apply -f elasticsearch.yaml
kubectl apply -f kibana.yaml
kubectl apply -f beats.yaml
echo "Deployment of ELK Done ."

echo "Creating secrets... " 
kubectl create configmap mysql-config --from-env-file=.env
kubectl create secret generic mysql-secret --from-env-file=.env
echo "Done."

