subscription_id = "4d894474-aa7f-4611-b830-344828c3eb9c" # use your own subscription ID.
pem_path = "cert/mycert.pem" # use your own

num_vm = 3

workerpool_size = 5

service_name = "azureipythontest" #fill this in
deployment_name = "azureipythontest" # fill this in
role_name = "azureipythontest" # fill this in
location = "East Asia"  #pick your data center
affinity_group = "my-ipython-group"  # fill
media_name = "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_2-LTS-amd64-server-20130624-en-us-30GB"  # may change use azure cli to list and find the right VM

media_link_base = "http://myipython.blob.core.windows.net/vhds/ipythonubuntu"

SERVICE_CERT_FORMAT = 'pfx' 
SERVICE_CERT_PASSWORD = 'Python'  #fill
#use azure cli to download the published profiles
SERVICE_CERT_DATA = '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'
SERVICE_CERT_DATA_PUBLIC = 'MIIC9jCCAeKgAwIBAgIQ00IFbqV9VqVJxI+wZka0szAJBgUrDgMCHQUAMBUxEzARBgNVBAMTClB5dGhvblRlc3QwHhcNMTIwODMwMDAyNTMzWhcNMzkxMjMxMjM1OTU5WjAVMRMwEQYDVQQDEwpQeXRob25UZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsjULNM53WPLkht1rbrDob/e4hZTHzj/hlLoBt2X3cNRc6dOPsMucxbMdchbCqAFa5RIaJvF5NDKqZuUSwq6bttD71twzy9bQ03EySOcRBad1VyqAZQ8DL8nUGSnXIUh+tpz4fDGM5f3Ly9NX8zfGqG3sT635rrFlUp3meJC+secCCwTLOOcIs3KQmuB+pMB5Y9rPhoxcekFfpq1pKtis6pmxnVbiL49kr6UUL6RQRDwik4t1jttatXLZqHETTmXl0Y0wS5AcJUXVAn5AL2kybULoThop2v01/E0NkPtFPAqLVs/kKBahniNn9uwUo+LS9FA8rWGu0FY4CZEYDfhb+QIDAQABo0owSDBGBgNVHQEEPzA9gBBS6knRHo54LppngxVCCzZVoRcwFTETMBEGA1UEAxMKUHl0aG9uVGVzdIIQ00IFaqV9VqVJxI+wZka0szAJBgUrDgMCHQUAA4IBAQAnZbP3YV+08wI4YTg6MOVA+j1njd0kVp35FLehripmaMNE6lgk3Vu1MGGl0JnvMr3fNFGFzRske/jVtFxlHE5H/CoUzmyMQ+W06eV/e995AduwTKsS0ZgYn0VoocSXWst/nyhpKOcbJgAOohOYxgsGI1JEqQgjyeqzcCIhw/vlWiA3V8bSiPnrC9vwhH0eB025hBd2VbEGDz2nWCYkwtuOLMTvkmLi/oFw3GOfgagZKk8k/ZPffMCafz+yR3vb1nqAjncrVcJLI8amUfpxhjZYexo8MbxBA432M6w8sjXN+uLCl7ByWZ4xs4vonWgkmjeObtU37SIzolHT4dxIgaP2'
SERVICE_CERT_THUMBPRINT = 'BBA4B74BD6B915E9DD6A01FB1B8C3C1740F517F2'

computer_name = "azurecomputer"
username = "azure"
password = "TestPassowrd"

endpoint = "9090" # default 9090
role_size = "Small" # default Small

notebook_passwd = "password"
# may not need to open these endpoints publicly this is for debugging purposes.
endpoint_list = [
        ("ssh", 'TCP', '22', '22'),
        ("ipython_public", 'TCP', '9090', '9090'),
        ("ipython0", 'TCP', '9191', '9191'),
        ("ipython1", 'TCP', '39292', '39292'),
        ("ipython2", 'TCP', '39393', '39393'),
        ("ipython3", 'TCP', '39494', '39494'),
        ("ipython4", 'TCP', '39595', '39595'),
        ("ipython5", 'TCP', '39696', '39696'),
        ("ipython6", 'TCP', '39797', '39797'),
        ("ipython7", 'TCP', '39898', '39898'),
        ("ipython8", 'TCP', '39999', '39999'),
        ("ipython10", 'TCP', '31000', '31000'),
        ("ipython11", 'TCP', '31001', '31001'),
        ("ipython12", 'TCP', '31002', '31002'),
        ]
