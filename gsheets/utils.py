import re

def get_specific_sheets(sheet: object, sheet_id: str, range: str) -> list:

    result = (
          sheet.values()
          .get(spreadsheetId=sheet_id, range=range)
          .execute()
      )
    values: list = result.get("values", [])
    return values

def get_all_sheets_data(sheet: object, sheet_id: str, without_headers: bool =False) -> list:
    """
    - properties:
        - gridProperties:
            - columnCount: 26
            - rowCount: 1000
        - index: 1
        - sheetId: 546508778
        - sheetType: 'GRID'
        - title: 'Sheet2'
    
    sheetId in properties is actually gid
    """
    spreadsheet_metadata = (
          sheet
          .get(spreadsheetId=sheet_id)
          .execute()
      )
    values = []
    for indivisual_sheet in spreadsheet_metadata.get("sheets", []):
        _: str = indivisual_sheet.get('properties', {}).get('sheetId')
        title: str = indivisual_sheet.get('properties', {}).get('title')
        
        _range = f"{title}"
        if without_headers == True:
            _range = _range + "!" +"A2:z999999"
        values.append(get_specific_sheets(sheet, sheet_id, range=_range))
    return values

def get_gid_sheets_data(sheet: object, sheet_id: str, gid:str, without_headers: bool =False) -> list:
    """
    sheetId in properties is actually gid

    if there are many sheets , we have following data corresponding to each sheet :
        - sheetId
        - title
        - index
        - sheetType
        - gridProperties

    for example :
        {
            'sheetId': 0, 
            'title': 'Sheet1',  # <- name that each sheet gets
            'index': 0,         # <- numerically the order of particular sheet
            'sheetType': 'GRID', 
            'gridProperties': {
                'rowCount': 1000, 
                'columnCount': 26
            }
            
        }

    In this function we are filtering based on `sheetId`( i.e gid )
    But we can also filter on `index` and `title` as well .

    """
    spreadsheet_metadata = sheet.get(
        spreadsheetId=sheet_id,
        fields='sheets.properties'  # Request only the properties of each sheet
    ).execute()
    
    found_sheet_properties = None
    if 'sheets' in spreadsheet_metadata:
        for indivisual_sheet in spreadsheet_metadata['sheets']:
            if str(indivisual_sheet['properties']['sheetId']) == gid:
                found_sheet_properties = indivisual_sheet['properties']
                break
        title: str = found_sheet_properties.get('title')
        _range = f"{title}"
        if without_headers == True:
            _range = _range + "!" +"A2:z999999"
        return get_specific_sheets(sheet, sheet_id, range=_range)
    return []

def extract_id_gid(url) -> tuple:
        """
        Extracts the ID and gid from a Google Sheet URL.

        Args:
            url: The Google Sheet URL.

        Returns:
            A tuple containing the ID and gid, or (None, None) if not found.
        """
        match = re.search(r"/d/([a-zA-Z0-9-_]+)(?:.*?gid=([0-9]+))?", url)
        if match:
            sheet_id = match.group(1)
            gid = match.group(2)
            return sheet_id, gid
        return None, None
    