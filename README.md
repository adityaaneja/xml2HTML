QUICK and Dirty Lambda function for converting xml to HTML

- The code boto3 to to work with s3 buckets
- The context passes the name of the source bucket and the filename with the xml extension 
- The lambda function is called on the S3_put event 
- destination_bucket is where the processed HTML file is placed
