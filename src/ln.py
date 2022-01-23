import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import os
import codecs

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
with open(os.path.expanduser('~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')
# Lnd cert is at ~/.lnd/tls.cert on Linux and
# ~/Library/Application Support/Lnd/tls.cert on Mac
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', creds)
stub = lnrpc.LightningStub(channel)

def get_invoice(amount):
    
    request = ln.Invoice(value=int(amount))
    response = stub.AddInvoice(request, metadata=[('macaroon', macaroon)])
    
    return [response.payment_request, response.r_hash]

def check_invoice(invoice):
    request = ln.PaymentHash(r_hash=invoice)
    response = stub.LookupInvoice(request, metadata=[('macaroon', macaroon)])
    return response.settled

def get_invoice_amount(invoice):
    request = ln.Invoice(payment_request=invoice)
    response = stub.AddInvoice(request, metadata=[('macaroon', macaroon)])
    invoice1 = response.r_hash
    
    request = ln.PaymentHash(r_hash=invoice1)
    response = stub.LookupInvoice(request, metadata=[('macaroon', macaroon)])
    print(response.value)
    return int(response.value)

def pay_invoice(invoice):
    request = ln.SendRequest(payment_request=invoice)
    response = stub.SendPaymentSync(request, metadata=[('macaroon', macaroon)])
    return response.payment_error