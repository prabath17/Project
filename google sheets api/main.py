import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1Fv1kPTTteISuHCQbvqO_nzAWNkeyLOM_nXhjBb-hZc0"  # to get in working google sheet url >  https://docs.google.com/spreadsheets/d/1Fv1kPTTteISuHCQbvqO_nzAWNkeyLOM_nXhjBb-hZc0/edit?gid=0#gid=0

'''
sheet = client.open_by_key(sheet_id)

val=sheet.sheet1.row_values(1)             #  to  print googlesheet data
print(val) '''

workbook=client.open_by_key(sheet_id)



'''sheets =map(lambda x:x.title,workbook.worksheets())  # to see how many worksheets are in this id 

print(list(sheets))

sheet =workbook.worksheet("Demo Sheet")
sheet.update_title("Demo Sheet") # to update the sheet title , once you updated you must be change.

sheet.update_acell("A1"," this is frist type to update a cell")
sheet.update_cell(1,2," this is second type to update a cell")

cell=sheet.find("prabath")
                                                     # to find the particular data in cell
print(cell.row,cell.col)          '''


values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
]

worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Values"

if new_worksheet_name in worksheet_list:
    sheet = workbook.worksheet(new_worksheet_name)
else:
    sheet = workbook.add_worksheet(new_worksheet_name, rows=10, cols=10)

sheet.clear()

sheet.update(f"A1:C{len(values)}", values)

sheet.format("A1:C1",{"textFormat":{"bold":True}})

sheet.update_cell(len(values) + 1, 2, "=sum(B2:B4)")
sheet.update_cell(len(values) + 1, 3, "=sum(C2:C4)")