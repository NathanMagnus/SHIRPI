import recaptcha.client.captcha as rc
 
public_key = '6Lf8aAkAAAAAAM5JDBdfmfsxnZv2WeGwF7b0zOEV'
private_key = '6Lf8aAkAAAAAAHN5OVHb-49SgXytXFsO79EscFdD'
 
def displayhtml(use_ssl=False, error=None):
    return rc.displayhtml(public_key, use_ssl, error)
 
def submit(request):
    return rc.submit(
        request.REQUEST.get('recaptcha_challenge_field',''),
        request.REQUEST.get('recaptcha_response_field',''),
        private_key,
        request.META.get('REMOTE_ADDR', ''))