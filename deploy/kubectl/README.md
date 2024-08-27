쿠버네티스에서 cert-manager를 사용하여 무료 Let’s Encrypt 인증서를 발급받는 방법은 다음과 같습니다. 이 과정은 쿠버네티스 클러스터에 cert-manager를 설치하고, ClusterIssuer를 설정한 후, 도메인에 대해 인증서를 발급받는 과정을 포함한다.

### 1. Cert-Manager 설치

cert-manager는 쿠버네티스 클러스터 내에서 인증서를 자동으로 관리해주는 툴입니다. Helm을 사용하여 설치할 수 있다.

##### 	1.	Helm 리포지토리 추가 및 업데이트
```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

##### 	2.	cert-manager 설치
아래 명령을 실행하여 cert-manager를 설치한다.

```bash
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.13.1/cert-manager.crds.yaml
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.13.1
```

##### 	3.	설치 확인
cert-manager가 제대로 설치되었는지 확인한다.
```bash
kubectl get pods --namespace cert-manager
```


### 2. ClusterIssuer 설정

Let’s Encrypt 인증서를 발급받기 위해 ClusterIssuer 또는 Issuer 리소스를 설정해야 한다. ClusterIssuer는 클러스터 전체에서 사용될 수 있다.

##### 	1.	ClusterIssuer 생성
Let’s Encrypt의 staging 또는 production 환경을 선택할 수 있다. staging 환경은 테스트용이며 발급 제한이 없다. 실제 운영 환경에서는 production을 사용한다.
아래는 ClusterIssuer 예시이다:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com  # Let's Encrypt 계정 이메일
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx  # 사용 중인 Ingress 클래스
```

이 파일을 cluster-issuer.yaml로 저장한 후 적용한다.

```bash
kubectl apply -f cluster-issuer.yaml
```

### 3. 인증서 요청 설정

이제 특정 도메인에 대해 인증서를 요청해야 합니다. 이를 위해 Certificate 리소스를 생성한다.

##### 	1.	Certificate 리소스 생성
아래는 Certificate 리소스 예시이다:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-certificate
  namespace: default  # 원하는 네임스페이스로 변경 가능
spec:
  secretName: my-certificate-tls  # 인증서가 저장될 Secret 이름
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: yourdomain.com
  dnsNames:
  - yourdomain.com
  - www.yourdomain.com
```

이 파일을 certificate.yaml로 저장한 후 적용한다.

```bash
kubectl apply -f certificate.yaml
```

##### 	2.	인증서 발급 상태 확인
인증서 발급 과정을 확인하려면 다음 명령을 사용한다:

```bash
kubectl describe certificate my-certificate -n default
```

인증서 발급이 성공적으로 이루어지면 my-certificate-tls라는 Secret이 생성된다. 이 Secret을 Ingress 리소스에서 참조하여 TLS 설정을 할 수 있다.

### 4. Ingress에 TLS 설정 추가

cert-manager가 발급한 인증서를 Ingress에서 사용하려면, Ingress 리소스에 TLS 설정을 추가해야 한다.

##### 1.	Ingress 리소스 설정
아래는 TLS가 적용된 Ingress 리소스 예시이다:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - yourdomain.com
    - www.yourdomain.com
    secretName: my-certificate-tls  # Certificate에서 생성된 Secret 이름
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

이 파일을 ingress.yaml로 저장한 후 적용한다.

```bash
kubectl apply -f ingress.yaml
```

### 5. 결과 확인

- Secret 생성 확인: `kubectl get secret my-certificate-tls -n default` 명령어로 인증서가 포함된 Secret이 생성되었는지 확인한다.
- Ingress TLS 확인: 브라우저를 통해 도메인에 접근하거나 `curl` 명령어를 사용해 HTTPS 연결이 성공적으로 설정되었는지 확인한다.

이 과정을 통해 쿠버네티스 클러스터에서 cert-manager와 Let’s Encrypt를 사용하여 무료 인증서를 발급하고, Ingress를 통해 HTTPS를 적용할 수 있다.
