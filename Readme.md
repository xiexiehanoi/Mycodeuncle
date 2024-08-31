# 코드 리뷰 워크플로우 설정 가이드

이 가이드는 GitHub Actions를 사용하여 코드 변경 사항에 대한 자동 코드 리뷰 워크플로우를 설정하는 방법을 설명합니다. Hugging Face 모델을 사용하여 코드 리뷰를 자동화합니다.

## 사용 방법

### 1. 리포지토리 생성
이 리포지토리를 템플릿으로 사용하여 새 리포지토리를 만듭니다.

### 2. 시크릿 추가하기
1. 새 리포지토리의 **Settings** 탭으로 이동합니다.
2. 좌측 사이드바에서 **Secrets and variables > Actions**를 클릭합니다.
3. **New repository secret** 버튼을 클릭하여 다음 시크릿을 추가합니다:
   - **HUGGINGFACE_API_KEY**: 본인의 Hugging Face API 키
   - **MODEL_NAME**: 사용할 모델 이름 (예: `bert-base-uncased`)

### 3. 워크플로우 파일 수정하기
`.github/workflows/code-review.yml` 파일을 열어 다음 부분을 확인하고 수정합니다:

- `uses:` 부분이 올바른 리포지토리를 가리키고 있는지 확인합니다. 필요시 수정합니다.

### 4. 코드 리뷰 자동 실행 확인
이제 push나 pull request를 생성할 때마다 자동으로 코드 리뷰가 실행됩니다!

> **참고**: 이 워크플로우는 기본적으로 `n8ntest` 리포지토리를 참조합니다. 다른 이름으로 포크했다면 해당 부분을 수정해야 합니다.

### 5. 워크플로우 스크립트 설정

`setup_code_review.sh` 스크립트를 사용하여 코드 리뷰 워크플로우를 설정합니다:

```bash
#!/bin/bash
# setup_code_review.sh

echo "Setting up code review workflow..."

# 현재 사용자 이름과 리포지토리 이름 가져오기
CURRENT_USER=$(git config user.name)
REPO_NAME=$(basename `git rev-parse --show-toplevel`)

# 워크플로우 파일 수정
sed -i '' "s/\${{ github.repository_owner }}/$CURRENT_USER/g" .github/workflows/code-review.yml
sed -i '' "s/n8ntest/$REPO_NAME/g" .github/workflows/code-review.yml

echo "Setup complete! Please add your HUGGINGFACE_API_KEY and MODEL_NAME to your repository secrets."
```
### 6. 문제 해결 (Troubleshooting)

- **API Key 오류**: Hugging Face API Key가 올바르지 않거나 만료된 경우, 새로운 키를 생성하여 다시 설정해야 합니다.
- **모델 이름 오류**: 모델 이름이 올바르지 않으면 리뷰가 실패할 수 있습니다. Hugging Face 모델 페이지에서 정확한 모델 이름을 확인하세요.

### 7. 추가 정보

- GitHub Actions 및 Secrets에 대한 자세한 내용은 [GitHub 문서](https://docs.github.com/en/actions/security-guides/encrypted-secrets)에서 확인할 수 있습니다.
- Hugging Face API 키는 [Hugging Face 계정](https://huggingface.co/settings/tokens)에서 발급받을 수 있습니다.

## 기여하기

이 프로젝트에 기여하고 싶다면, PR을 보내주세요! 문제점이나 개선 사항이 있다면 Issue를 열어주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

