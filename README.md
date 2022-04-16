# COUNTIES-API-SERVICE

## PRECURETIONS

หลังจาก clone ไปแล้ว 

> สร้าง virtual env ขึ้นมา (ลองหาวิธีใน google นะจ๊ะ)
> 
> Create virtual env
> 
> python -m venv myenv
> 
> myenv/scripts/activate เพื่อเปิดใช้ venv
> 
> pip install -r requirements.txt เพื่อ downloads dependency packages
> 
>  uvicorn main:app --reload เพื่อเปิดใช้ server
## Prepare Data & regular expression (functions ที่ใช้ prepare data ใน database และ regular expression)
/prepare_data.py
## API SERVICE (Application สำหรับให้ฝั่ง Client เรียกใช้)
/ main.py 
## Database 
/database/data.json
## associate
[FRONT END](https://github.com/aphisit-ths/TOC-ASSIGNMENT-FRONTEND) 
