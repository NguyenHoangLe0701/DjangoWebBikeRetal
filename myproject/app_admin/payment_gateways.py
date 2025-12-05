"""
Payment Gateway Integration
Support for VNPay, MoMo, ZaloPay
"""
import hmac
import hashlib
import urllib.parse
from django.conf import settings
from django.urls import reverse
from datetime import datetime

class VNPayGateway:
    """VNPay Payment Gateway Integration"""
    
    def __init__(self):
        self.vnp_TmnCode = getattr(settings, 'VNPAY_TMN_CODE', '')
        self.vnp_HashSecret = getattr(settings, 'VNPAY_HASH_SECRET', '')
        self.vnp_Url = getattr(settings, 'VNPAY_URL', 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html')
        self.vnp_ReturnUrl = getattr(settings, 'VNPAY_RETURN_URL', '')
    
    def create_payment_url(self, amount, order_id, order_info, ip_address, locale='vn'):
        """
        Tạo payment URL cho VNPay
        
        Args:
            amount: Số tiền (VNĐ)
            order_id: Mã đơn hàng
            order_info: Thông tin đơn hàng
            ip_address: IP của khách hàng
            locale: Ngôn ngữ (vn/en)
        
        Returns:
            Payment URL
        """
        vnp_Params = {}
        vnp_Params['vnp_Version'] = '2.1.0'
        vnp_Params['vnp_Command'] = 'pay'
        vnp_Params['vnp_TmnCode'] = self.vnp_TmnCode
        vnp_Params['vnp_Amount'] = int(amount) * 100  # VNPay expects amount in cents
        vnp_Params['vnp_CurrCode'] = 'VND'
        vnp_Params['vnp_TxnRef'] = order_id
        vnp_Params['vnp_OrderInfo'] = order_info
        vnp_Params['vnp_OrderType'] = 'other'
        vnp_Params['vnp_Locale'] = locale
        vnp_Params['vnp_ReturnUrl'] = self.vnp_ReturnUrl
        vnp_Params['vnp_IpAddr'] = ip_address
        vnp_Params['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Sort params
        vnp_Params = dict(sorted(vnp_Params.items()))
        
        # Create query string
        query_string = urllib.parse.urlencode(vnp_Params)
        
        # Create secure hash
        sign_data = query_string
        if self.vnp_HashSecret:
            hmac_sha512 = hmac.new(
                bytes(self.vnp_HashSecret, 'utf-8'),
                bytes(sign_data, 'utf-8'),
                hashlib.sha512
            ).hexdigest()
            vnp_Params['vnp_SecureHash'] = hmac_sha512
        
        # Build payment URL
        payment_url = self.vnp_Url + '?' + urllib.parse.urlencode(vnp_Params)
        return payment_url
    
    def verify_payment(self, request_data):
        """
        Verify payment callback từ VNPay
        
        Args:
            request_data: Query parameters từ VNPay callback
        
        Returns:
            dict với status và transaction info
        """
        vnp_Params = {}
        for key, value in request_data.items():
            if key.startswith('vnp_'):
                vnp_Params[key] = value
        
        # Get secure hash
        vnp_SecureHash = vnp_Params.pop('vnp_SecureHash', '')
        
        # Sort params
        vnp_Params = dict(sorted(vnp_Params.items()))
        
        # Create query string
        query_string = urllib.parse.urlencode(vnp_Params)
        
        # Verify hash
        sign_data = query_string
        if self.vnp_HashSecret:
            hmac_sha512 = hmac.new(
                bytes(self.vnp_HashSecret, 'utf-8'),
                bytes(sign_data, 'utf-8'),
                hashlib.sha512
            ).hexdigest()
            
            if hmac_sha512 != vnp_SecureHash:
                return {
                    'status': 'failed',
                    'message': 'Invalid secure hash'
                }
        
        # Check response code
        vnp_ResponseCode = vnp_Params.get('vnp_ResponseCode', '')
        
        if vnp_ResponseCode == '00':
            return {
                'status': 'success',
                'transaction_id': vnp_Params.get('vnp_TxnRef', ''),
                'gateway_transaction_id': vnp_Params.get('vnp_TransactionNo', ''),
                'amount': int(vnp_Params.get('vnp_Amount', 0)) / 100,  # Convert from cents
                'gateway_response': vnp_Params
            }
        else:
            return {
                'status': 'failed',
                'message': f'Payment failed with code: {vnp_ResponseCode}',
                'gateway_response': vnp_Params
            }

class MoMoGateway:
    """MoMo Payment Gateway Integration (Placeholder)"""
    
    def __init__(self):
        self.partner_code = getattr(settings, 'MOMO_PARTNER_CODE', '')
        self.access_key = getattr(settings, 'MOMO_ACCESS_KEY', '')
        self.secret_key = getattr(settings, 'MOMO_SECRET_KEY', '')
        self.api_url = getattr(settings, 'MOMO_API_URL', 'https://test-payment.momo.vn/v2/gateway/api/create')
    
    def create_payment_url(self, amount, order_id, order_info, ip_address):
        """Tạo payment URL cho MoMo (Placeholder - cần implement)"""
        # TODO: Implement MoMo integration
        return None
    
    def verify_payment(self, request_data):
        """Verify payment callback từ MoMo (Placeholder)"""
        # TODO: Implement MoMo verification
        return {'status': 'failed', 'message': 'MoMo integration not implemented'}

class ZaloPayGateway:
    """ZaloPay Payment Gateway Integration (Placeholder)"""
    
    def __init__(self):
        self.app_id = getattr(settings, 'ZALOPAY_APP_ID', '')
        self.key1 = getattr(settings, 'ZALOPAY_KEY1', '')
        self.key2 = getattr(settings, 'ZALOPAY_KEY2', '')
        self.api_url = getattr(settings, 'ZALOPAY_API_URL', 'https://sandbox.zalopay.com.vn/v001/tpe/createorder')
    
    def create_payment_url(self, amount, order_id, order_info, ip_address):
        """Tạo payment URL cho ZaloPay (Placeholder - cần implement)"""
        # TODO: Implement ZaloPay integration
        return None
    
    def verify_payment(self, request_data):
        """Verify payment callback từ ZaloPay (Placeholder)"""
        # TODO: Implement ZaloPay verification
        return {'status': 'failed', 'message': 'ZaloPay integration not implemented'}

def get_payment_gateway(gateway_name):
    """Factory function để get payment gateway"""
    gateways = {
        'vnpay': VNPayGateway,
        'momo': MoMoGateway,
        'zalopay': ZaloPayGateway,
    }
    
    gateway_class = gateways.get(gateway_name.lower())
    if gateway_class:
        return gateway_class()
    return None

