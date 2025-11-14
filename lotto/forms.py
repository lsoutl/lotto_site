from django import forms

class ManualPurchaseForm(forms.Form):
    numbers = forms.CharField(
        label="번호(6개)", help_text="예: 1,3,12,21,33,42 (쉼표로 6개)"
    )
    def clean_numbers(self):
        raw = self.cleaned_data["numbers"].replace(" ", "")
        try:
            nums = [int(x) for x in raw.split(",")]
        except Exception:
            raise forms.ValidationError("숫자만 입력하세요.")
        if len(nums) != 6 or len(set(nums)) != 6:
            raise forms.ValidationError("서로 다른 6개 번호여야 합니다.")
        if not all(1 <= n <= 45 for n in nums):
            raise forms.ValidationError("번호는 1~45 범위여야 합니다.")
        return sorted(nums)