<powershell>
aws s3 cp s3://my-app-bucket/latest-app.zip C:\temp\app.zip --region us-east-1
Expand-Archive -Path C:\temp\app.zip -DestinationPath C:\app -Force
C:\app\setup.exe /silent /install
</powershell>
