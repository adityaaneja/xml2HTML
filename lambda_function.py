import os
import boto3
from subprocess import check_output
import re
import lxml.html
from lxml import etree
from lxml import html
import urllib

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    filename = os.path.splitext(key)[0]
    destination_bucket = 'ca.ualberta.edrms.htmlin'
    outputfilename = os.path.join(filename+".html")
    
    
    s3source = boto3.resource('s3')
   # obj=s3source.Object(bucket, key)
   # obj.get()["Body"].read()
    
    #EXTRACT XSLT URL
    tempxmlfile=os.path.join("/tmp/" + filename +".xml")
    s3source.Bucket(bucket).download_file(key,tempxmlfile)
    url=check_output(["cat", tempxmlfile])
    xslt_url=re.findall(r'(https?://\S+\.xsl)',url)[0]
    

    #Save the XSLT
    tempxsltfile=os.path.join("/tmp/" + filename +".xslt")
    xslt_to_download = urllib.URLopener()
    xslt_to_download.retrieve(xslt_url,tempxsltfile)

    #Apply the XSLT on the XML
    data = open(tempxsltfile)
    xslt_content = data.read()
    xslt_root = etree.XML(xslt_content)
    transform = etree.XSLT(xslt_root)
    
    dom = etree.parse(tempxmlfile)
    result = transform(dom)
    
    #write the newly created html
    tempoutputfilename = os.path.join("/tmp/" + filename +".html")
    output_file = open(tempoutputfilename, 'w')
    output_file.write(str(result))
    output_file.close()

    print check_output(["cat", tempoutputfilename])

    s3destination = boto3.resource('s3')
    html_data = open(tempoutputfilename,'rb')
    s3destination.Bucket(destination_bucket).put_object(Key=outputfilename, Body=html_data)

