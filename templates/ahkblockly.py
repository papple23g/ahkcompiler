#{% verbatim %}

from browser import ajax, timer

#全域變數
Blockly=window.Blockly
workspace=window.workspace
TAB_SPACE="    "  #縮排

#region 腳本函數字典
FUNC_DICT={
    #螢幕寬高
    'screen_width':{
        'pre':'SysGet, VirtualWidth, 78\n'
    },
    'screen_height':{
        'pre':'SysGet, VirtualHeight, 79\n'
    },
    #region ArrayStr
    'ArrayStr':{
        'end':
'''
;定義函數:判斷是否為Array
IsArray(oArray)
{
    if (ArrayStr(oArray)=="[]") {
        oArray.Push(1)
        if (oArray.MaxIndex())
            return True
        return False
    } else {
        return True
    }
}
;定義函數，串列字串化
ArrayStr(arr) {
    com_str := "["
    for i_index, i in arr
    {
        if IsArray(i) {
            com_str .= ArrayStr(i)
        } else {
            com_str .= i
        }
        com_str .= ", "
    }
    com_str := SubStr(com_str,1,StrLen(com_str)-2)
    com_str .= "]"
    if (com_str="]")
        return "[]"
    return com_str
}
'''
    },
    #endregion ArrayStr
    'SetBrightness':{
        'pre':"__vBright := 100\n",
        'end':"\n".join([
            f"; ref. https://www.autohotkey.com/boards/viewtopic.php?f=6&t=39580",
            f";'z dimmer.ahk' by jeeswg",
            f'SetBrightness(__vBright){{',
            f'{TAB_SPACE}OnMessage(0x5555, "MsgMonitor")',
            f'{TAB_SPACE}OnMessage(0x5556, "MsgMonitor2")',
            f'{TAB_SPACE}OnMessage(0x5557, "MsgMonitor3")',
            f'{TAB_SPACE}WinGet, hWnd, ID, A',
            f'{TAB_SPACE}vNum := Round(((100-__vBright)/100) * 255)',
            f'{TAB_SPACE}Gui, Color, 000000',
            f'{TAB_SPACE};WS_EX_TRANSPARENT := 0x20 (click-through)',
            f'{TAB_SPACE}Gui, -Caption +AlwaysOnTop +E0x20 +HwndhGui +ToolWindow',
            f'{TAB_SPACE};獲取顯示器總數',
            f'{TAB_SPACE}SysGet, __nb_monitor, MonitorCount',
            f'{TAB_SPACE}Gui, Show, % Format("x0 y0 w{{}} h{{}}", A_ScreenWidth*__nb_monitor, A_ScreenHeight), dimmer',
            f'{TAB_SPACE}WinSet, Transparent, % vNum, % "ahk_id " hGui',
            f'{TAB_SPACE}WinActivate, % "ahk_id " hWnd',
            f'{TAB_SPACE}return',
            "}",
            ";hide window (turn dimmer off)",
            "MsgMonitor(wParam, lParam, uMsg)",
            "{",
            f'{TAB_SPACE}global',
            f'{TAB_SPACE}Gui, Hide',
            "}",
            ";show window (turn dimmer on)",
            "MsgMonitor2(wParam, lParam, uMsg)",
            "{",
            f'{TAB_SPACE}global',
            f'{TAB_SPACE}WinGet, hWnd, ID, A',
            f'{TAB_SPACE}Gui, Show',
            f'{TAB_SPACE}WinActivate, % "ahk_id " hWnd',
            "}",
            ";return dimmer level",
            "MsgMonitor3(wParam, lParam, msg)",
            "{",
            f'{TAB_SPACE}global',
            f'{TAB_SPACE}return __vBright',
            "}\n"
        ])
    },
    'SetTitleMatchMode':{
        'pre':"SetTitleMatchMode, 2\n"
    },
    'FullwidthSymbol':{
        'end':
''';轉換符號為全行字，避免檔案名稱出錯
FullwidthSymbol(input_text){
    input_text:=StrReplace(input_text,"\","＼")
    input_text:=StrReplace(input_text,"/","／")
    input_text:=StrReplace(input_text,":","：")
    input_text:=StrReplace(input_text,"*","＊")
    input_text:=StrReplace(input_text,"?","？")
    input_text:=StrReplace(input_text,"<","＜")
    input_text:=StrReplace(input_text,">","＞")
    input_text:=StrReplace(input_text,"|","｜")
    return input_text
}
'''},
    #region Screenshot
    'Screenshot':{
        'end':
'''; Gdip standard library v1.45 by tic (Tariq Porter) 07/09/11
; Modifed by Rseding91 using fincs 64 bit compatible Gdip library 5/1/2013
; Supports: Basic, _L ANSi, _L Unicode x86 and _L Unicode x64
;
; Updated 2/20/2014 - fixed Gdip_CreateRegion() and Gdip_GetClipRegion() on AHK Unicode x86
; Updated 5/13/2013 - fixed Gdip_SetBitmapToClipboard() on AHK Unicode x64
;
;-------------------------------------------------------------------------------------
;-------------------------------------------------------------------------------------
; STATUS ENUMERATION
; Return values for functions specified to have status enumerated return type
;-------------------------------------------------------------------------------------
;
; Ok =						= 0
; GenericError				= 1
; InvalidParameter			= 2
; OutOfMemory				= 3
; ObjectBusy				= 4
; InsufficientBuffer		= 5
; NotImplemented			= 6
; Win32Error				= 7
; WrongState				= 8
; Aborted					= 9
; FileNotFound				= 10
; ValueOverflow				= 11
; AccessDenied				= 12
; UnknownImageFormat		= 13
; FontFamilyNotFound		= 14
; FontStyleNotFound			= 15
; NotTrueTypeFont			= 16
; UnsupportedGdiplusVersion	= 17
; GdiplusNotInitialized		= 18
; PropertyNotFound			= 19
; PropertyNotSupported		= 20
; ProfileNotFound			= 21
;
;-------------------------------------------------------------------------------------
;-------------------------------------------------------------------------------------
; FUNCTIONS
;-------------------------------------------------------------------------------------
;
; UpdateLayeredWindow(hwnd, hdc, x="", y="", w="", h="", Alpha=255)
; BitBlt(ddc, dx, dy, dw, dh, sdc, sx, sy, Raster="")
; StretchBlt(dDC, dx, dy, dw, dh, sDC, sx, sy, sw, sh, Raster="")
; SetImage(hwnd, hBitmap)
; Gdip_BitmapFromScreen(Screen=0, Raster="")
; CreateRectF(ByRef RectF, x, y, w, h)
; CreateSizeF(ByRef SizeF, w, h)
; CreateDIBSection
;
;-------------------------------------------------------------------------------------

; Function:     			UpdateLayeredWindow
; Description:  			Updates a layered window with the handle to the DC of a gdi bitmap
; 
; hwnd        				Handle of the layered window to update
; hdc           			Handle to the DC of the GDI bitmap to update the window with
; Layeredx      			x position to place the window
; Layeredy      			y position to place the window
; Layeredw      			Width of the window
; Layeredh      			Height of the window
; Alpha         			Default = 255 : The transparency (0-255) to set the window transparency
;
; return      				If the function succeeds, the return value is nonzero
;
; notes						If x or y omitted, then layered window will use its current coordinates
;							If w or h omitted then current width and height will be used

UpdateLayeredWindow(hwnd, hdc, x="", y="", w="", h="", Alpha=255)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if ((x != "") && (y != ""))
		VarSetCapacity(pt, 8), NumPut(x, pt, 0, "UInt"), NumPut(y, pt, 4, "UInt")

	if (w = "") ||(h = "")
		WinGetPos,,, w, h, ahk_id %hwnd%
   
	return DllCall("UpdateLayeredWindow"
					, Ptr, hwnd
					, Ptr, 0
					, Ptr, ((x = "") && (y = "")) ? 0 : &pt
					, "int64*", w|h<<32
					, Ptr, hdc
					, "int64*", 0
					, "uint", 0
					, "UInt*", Alpha<<16|1<<24
					, "uint", 2)
}

;-------------------------------------------------------------------------------------

; Function				BitBlt
; Description			The BitBlt function performs a bit-block transfer of the color data corresponding to a rectangle 
;						of pixels from the specified source device context into a destination device context.
;
; dDC					handle to destination DC
; dx					x-coord of destination upper-left corner
; dy					y-coord of destination upper-left corner
; dw					width of the area to copy
; dh					height of the area to copy
; sDC					handle to source DC
; sx					x-coordinate of source upper-left corner
; sy					y-coordinate of source upper-left corner
; Raster				raster operation code
;
; return				If the function succeeds, the return value is nonzero
;
; notes					If no raster operation is specified, then SRCCOPY is used, which copies the source directly to the destination rectangle
;
; BLACKNESS				= 0x00000042
; NOTSRCERASE			= 0x001100A6
; NOTSRCCOPY			= 0x00330008
; SRCERASE				= 0x00440328
; DSTINVERT				= 0x00550009
; PATINVERT				= 0x005A0049
; SRCINVERT				= 0x00660046
; SRCAND				= 0x008800C6
; MERGEPAINT			= 0x00BB0226
; MERGECOPY				= 0x00C000CA
; SRCCOPY				= 0x00CC0020
; SRCPAINT				= 0x00EE0086
; PATCOPY				= 0x00F00021
; PATPAINT				= 0x00FB0A09
; WHITENESS				= 0x00FF0062
; CAPTUREBLT			= 0x40000000
; NOMIRRORBITMAP		= 0x80000000

BitBlt(ddc, dx, dy, dw, dh, sdc, sx, sy, Raster="")
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdi32\BitBlt"
					, Ptr, dDC
					, "int", dx
					, "int", dy
					, "int", dw
					, "int", dh
					, Ptr, sDC
					, "int", sx
					, "int", sy
					, "uint", Raster ? Raster : 0x00CC0020)
}

;-------------------------------------------------------------------------------------

; Function				StretchBlt
; Description			The StretchBlt function copies a bitmap from a source rectangle into a destination rectangle, 
;						stretching or compressing the bitmap to fit the dimensions of the destination rectangle, if necessary.
;						The system stretches or compresses the bitmap according to the stretching mode currently set in the destination device context.
;
; ddc					handle to destination DC
; dx					x-coord of destination upper-left corner
; dy					y-coord of destination upper-left corner
; dw					width of destination rectangle
; dh					height of destination rectangle
; sdc					handle to source DC
; sx					x-coordinate of source upper-left corner
; sy					y-coordinate of source upper-left corner
; sw					width of source rectangle
; sh					height of source rectangle
; Raster				raster operation code
;
; return				If the function succeeds, the return value is nonzero
;
; notes					If no raster operation is specified, then SRCCOPY is used. It uses the same raster operations as BitBlt		

StretchBlt(ddc, dx, dy, dw, dh, sdc, sx, sy, sw, sh, Raster="")
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdi32\StretchBlt"
					, Ptr, ddc
					, "int", dx
					, "int", dy
					, "int", dw
					, "int", dh
					, Ptr, sdc
					, "int", sx
					, "int", sy
					, "int", sw
					, "int", sh
					, "uint", Raster ? Raster : 0x00CC0020)
}

;-------------------------------------------------------------------------------------

; Function				SetStretchBltMode
; Description			The SetStretchBltMode function sets the bitmap stretching mode in the specified device context
;
; hdc					handle to the DC
; iStretchMode			The stretching mode, describing how the target will be stretched
;
; return				If the function succeeds, the return value is the previous stretching mode. If it fails it will return 0
;
; STRETCH_ANDSCANS 		= 0x01
; STRETCH_ORSCANS 		= 0x02
; STRETCH_DELETESCANS 	= 0x03
; STRETCH_HALFTONE 		= 0x04

SetStretchBltMode(hdc, iStretchMode=4)
{
	return DllCall("gdi32\SetStretchBltMode"
					, A_PtrSize ? "UPtr" : "UInt", hdc
					, "int", iStretchMode)
}

;-------------------------------------------------------------------------------------

; Function				SetImage
; Description			Associates a new image with a static control
;
; hwnd					handle of the control to update
; hBitmap				a gdi bitmap to associate the static control with
;
; return				If the function succeeds, the return value is nonzero

SetImage(hwnd, hBitmap)
{
	SendMessage, 0x172, 0x0, hBitmap,, ahk_id %hwnd%
	E := ErrorLevel
	DeleteObject(E)
	return E
}

;-------------------------------------------------------------------------------------

; Function				SetSysColorToControl
; Description			Sets a solid colour to a control
;
; hwnd					handle of the control to update
; SysColor				A system colour to set to the control
;
; return				If the function succeeds, the return value is zero
;
; notes					A control must have the 0xE style set to it so it is recognised as a bitmap
;						By default SysColor=15 is used which is COLOR_3DFACE. This is the standard background for a control
;
; COLOR_3DDKSHADOW				= 21
; COLOR_3DFACE					= 15
; COLOR_3DHIGHLIGHT				= 20
; COLOR_3DHILIGHT				= 20
; COLOR_3DLIGHT					= 22
; COLOR_3DSHADOW				= 16
; COLOR_ACTIVEBORDER			= 10
; COLOR_ACTIVECAPTION			= 2
; COLOR_APPWORKSPACE			= 12
; COLOR_BACKGROUND				= 1
; COLOR_BTNFACE					= 15
; COLOR_BTNHIGHLIGHT			= 20
; COLOR_BTNHILIGHT				= 20
; COLOR_BTNSHADOW				= 16
; COLOR_BTNTEXT					= 18
; COLOR_CAPTIONTEXT				= 9
; COLOR_DESKTOP					= 1
; COLOR_GRADIENTACTIVECAPTION	= 27
; COLOR_GRADIENTINACTIVECAPTION	= 28
; COLOR_GRAYTEXT				= 17
; COLOR_HIGHLIGHT				= 13
; COLOR_HIGHLIGHTTEXT			= 14
; COLOR_HOTLIGHT				= 26
; COLOR_INACTIVEBORDER			= 11
; COLOR_INACTIVECAPTION			= 3
; COLOR_INACTIVECAPTIONTEXT		= 19
; COLOR_INFOBK					= 24
; COLOR_INFOTEXT				= 23
; COLOR_MENU					= 4
; COLOR_MENUHILIGHT				= 29
; COLOR_MENUBAR					= 30
; COLOR_MENUTEXT				= 7
; COLOR_SCROLLBAR				= 0
; COLOR_WINDOW					= 5
; COLOR_WINDOWFRAME				= 6
; COLOR_WINDOWTEXT				= 8

SetSysColorToControl(hwnd, SysColor=15)
{
   WinGetPos,,, w, h, ahk_id %hwnd%
   bc := DllCall("GetSysColor", "Int", SysColor, "UInt")
   pBrushClear := Gdip_BrushCreateSolid(0xff000000 | (bc >> 16 | bc & 0xff00 | (bc & 0xff) << 16))
   pBitmap := Gdip_CreateBitmap(w, h), G := Gdip_GraphicsFromImage(pBitmap)
   Gdip_FillRectangle(G, pBrushClear, 0, 0, w, h)
   hBitmap := Gdip_CreateHBITMAPFromBitmap(pBitmap)
   SetImage(hwnd, hBitmap)
   Gdip_DeleteBrush(pBrushClear)
   Gdip_DeleteGraphics(G), Gdip_DisposeImage(pBitmap), DeleteObject(hBitmap)
   return 0
}

;-------------------------------------------------------------------------------------

; Function				Gdip_BitmapFromScreen
; Description			Gets a gdi+ bitmap from the screen
;
; Screen				0 = All screens
;						Any numerical value = Just that screen
;						x|y|w|h = Take specific coordinates with a width and height
; Raster				raster operation code
;
; return      			If the function succeeds, the return value is a pointer to a gdi+ bitmap
;						-1:		one or more of x,y,w,h not passed properly
;
; notes					If no raster operation is specified, then SRCCOPY is used to the returned bitmap

Gdip_BitmapFromScreen(Screen=0, Raster="")
{
	if (Screen = 0)
	{
		Sysget, x, 76
		Sysget, y, 77	
		Sysget, w, 78
		Sysget, h, 79
	}
	else if (SubStr(Screen, 1, 5) = "hwnd:")
	{
		Screen := SubStr(Screen, 6)
		if !WinExist( "ahk_id " Screen)
			return -2
		WinGetPos,,, w, h, ahk_id %Screen%
		x := y := 0
		hhdc := GetDCEx(Screen, 3)
	}
	else if (Screen&1 != "")
	{
		Sysget, M, Monitor, %Screen%
		x := MLeft, y := MTop, w := MRight-MLeft, h := MBottom-MTop
	}
	else
	{
		StringSplit, S, Screen, |
		x := S1, y := S2, w := S3, h := S4
	}

	if (x = "") || (y = "") || (w = "") || (h = "")
		return -1

	chdc := CreateCompatibleDC(), hbm := CreateDIBSection(w, h, chdc), obm := SelectObject(chdc, hbm), hhdc := hhdc ? hhdc : GetDC()
	BitBlt(chdc, 0, 0, w, h, hhdc, x, y, Raster)
	ReleaseDC(hhdc)
	
	pBitmap := Gdip_CreateBitmapFromHBITMAP(hbm)
	SelectObject(chdc, obm), DeleteObject(hbm), DeleteDC(hhdc), DeleteDC(chdc)
	return pBitmap
}

;-------------------------------------------------------------------------------------

; Function				Gdip_BitmapFromHWND
; Description			Uses PrintWindow to get a handle to the specified window and return a bitmap from it
;
; hwnd					handle to the window to get a bitmap from
;
; return				If the function succeeds, the return value is a pointer to a gdi+ bitmap
;
; notes					Window must not be not minimised in order to get a handle to it's client area

Gdip_BitmapFromHWND(hwnd)
{
	WinGetPos,,, Width, Height, ahk_id %hwnd%
	hbm := CreateDIBSection(Width, Height), hdc := CreateCompatibleDC(), obm := SelectObject(hdc, hbm)
	PrintWindow(hwnd, hdc)
	pBitmap := Gdip_CreateBitmapFromHBITMAP(hbm)
	SelectObject(hdc, obm), DeleteObject(hbm), DeleteDC(hdc)
	return pBitmap
}

;-------------------------------------------------------------------------------------

; Function    			CreateRectF
; Description			Creates a RectF object, containing a the coordinates and dimensions of a rectangle
;
; RectF       			Name to call the RectF object
; x            			x-coordinate of the upper left corner of the rectangle
; y            			y-coordinate of the upper left corner of the rectangle
; w            			Width of the rectangle
; h            			Height of the rectangle
;
; return      			No return value

CreateRectF(ByRef RectF, x, y, w, h)
{
   VarSetCapacity(RectF, 16)
   NumPut(x, RectF, 0, "float"), NumPut(y, RectF, 4, "float"), NumPut(w, RectF, 8, "float"), NumPut(h, RectF, 12, "float")
}

;-------------------------------------------------------------------------------------

; Function    			CreateRect
; Description			Creates a Rect object, containing a the coordinates and dimensions of a rectangle
;
; RectF       			Name to call the RectF object
; x            			x-coordinate of the upper left corner of the rectangle
; y            			y-coordinate of the upper left corner of the rectangle
; w            			Width of the rectangle
; h            			Height of the rectangle
;
; return      			No return value

CreateRect(ByRef Rect, x, y, w, h)
{
	VarSetCapacity(Rect, 16)
	NumPut(x, Rect, 0, "uint"), NumPut(y, Rect, 4, "uint"), NumPut(w, Rect, 8, "uint"), NumPut(h, Rect, 12, "uint")
}
;-------------------------------------------------------------------------------------

; Function		    	CreateSizeF
; Description			Creates a SizeF object, containing an 2 values
;
; SizeF         		Name to call the SizeF object
; w            			w-value for the SizeF object
; h            			h-value for the SizeF object
;
; return      			No Return value

CreateSizeF(ByRef SizeF, w, h)
{
   VarSetCapacity(SizeF, 8)
   NumPut(w, SizeF, 0, "float"), NumPut(h, SizeF, 4, "float")     
}
;-------------------------------------------------------------------------------------

; Function		    	CreatePointF
; Description			Creates a SizeF object, containing an 2 values
;
; SizeF         		Name to call the SizeF object
; w            			w-value for the SizeF object
; h            			h-value for the SizeF object
;
; return      			No Return value

CreatePointF(ByRef PointF, x, y)
{
   VarSetCapacity(PointF, 8)
   NumPut(x, PointF, 0, "float"), NumPut(y, PointF, 4, "float")     
}
;-------------------------------------------------------------------------------------

; Function				CreateDIBSection
; Description			The CreateDIBSection function creates a DIB (Device Independent Bitmap) that applications can write to directly
;
; w						width of the bitmap to create
; h						height of the bitmap to create
; hdc					a handle to the device context to use the palette from
; bpp					bits per pixel (32 = ARGB)
; ppvBits				A pointer to a variable that receives a pointer to the location of the DIB bit values
;
; return				returns a DIB. A gdi bitmap
;
; notes					ppvBits will receive the location of the pixels in the DIB

CreateDIBSection(w, h, hdc="", bpp=32, ByRef ppvBits=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	hdc2 := hdc ? hdc : GetDC()
	VarSetCapacity(bi, 40, 0)
	
	NumPut(w, bi, 4, "uint")
	, NumPut(h, bi, 8, "uint")
	, NumPut(40, bi, 0, "uint")
	, NumPut(1, bi, 12, "ushort")
	, NumPut(0, bi, 16, "uInt")
	, NumPut(bpp, bi, 14, "ushort")
	
	hbm := DllCall("CreateDIBSection"
					, Ptr, hdc2
					, Ptr, &bi
					, "uint", 0
					, A_PtrSize ? "UPtr*" : "uint*", ppvBits
					, Ptr, 0
					, "uint", 0, Ptr)

	if !hdc
		ReleaseDC(hdc2)
	return hbm
}

;-------------------------------------------------------------------------------------

; Function				PrintWindow
; Description			The PrintWindow function copies a visual window into the specified device context (DC), typically a printer DC
;
; hwnd					A handle to the window that will be copied
; hdc					A handle to the device context
; Flags					Drawing options
;
; return				If the function succeeds, it returns a nonzero value
;
; PW_CLIENTONLY			= 1

PrintWindow(hwnd, hdc, Flags=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("PrintWindow", Ptr, hwnd, Ptr, hdc, "uint", Flags)
}

;-------------------------------------------------------------------------------------

; Function				DestroyIcon
; Description			Destroys an icon and frees any memory the icon occupied
;
; hIcon					Handle to the icon to be destroyed. The icon must not be in use
;
; return				If the function succeeds, the return value is nonzero

DestroyIcon(hIcon)
{
	return DllCall("DestroyIcon", A_PtrSize ? "UPtr" : "UInt", hIcon)
}

;-------------------------------------------------------------------------------------

PaintDesktop(hdc)
{
	return DllCall("PaintDesktop", A_PtrSize ? "UPtr" : "UInt", hdc)
}

;-------------------------------------------------------------------------------------

CreateCompatibleBitmap(hdc, w, h)
{
	return DllCall("gdi32\CreateCompatibleBitmap", A_PtrSize ? "UPtr" : "UInt", hdc, "int", w, "int", h)
}

;-------------------------------------------------------------------------------------

; Function				CreateCompatibleDC
; Description			This function creates a memory device context (DC) compatible with the specified device
;
; hdc					Handle to an existing device context					
;
; return				returns the handle to a device context or 0 on failure
;
; notes					If this handle is 0 (by default), the function creates a memory device context compatible with the application's current screen

CreateCompatibleDC(hdc=0)
{
   return DllCall("CreateCompatibleDC", A_PtrSize ? "UPtr" : "UInt", hdc)
}

;-------------------------------------------------------------------------------------

; Function				SelectObject
; Description			The SelectObject function selects an object into the specified device context (DC). The new object replaces the previous object of the same type
;
; hdc					Handle to a DC
; hgdiobj				A handle to the object to be selected into the DC
;
; return				If the selected object is not a region and the function succeeds, the return value is a handle to the object being replaced
;
; notes					The specified object must have been created by using one of the following functions
;						Bitmap - CreateBitmap, CreateBitmapIndirect, CreateCompatibleBitmap, CreateDIBitmap, CreateDIBSection (A single bitmap cannot be selected into more than one DC at the same time)
;						Brush - CreateBrushIndirect, CreateDIBPatternBrush, CreateDIBPatternBrushPt, CreateHatchBrush, CreatePatternBrush, CreateSolidBrush
;						Font - CreateFont, CreateFontIndirect
;						Pen - CreatePen, CreatePenIndirect
;						Region - CombineRgn, CreateEllipticRgn, CreateEllipticRgnIndirect, CreatePolygonRgn, CreateRectRgn, CreateRectRgnIndirect
;
; notes					If the selected object is a region and the function succeeds, the return value is one of the following value
;
; SIMPLEREGION			= 2 Region consists of a single rectangle
; COMPLEXREGION			= 3 Region consists of more than one rectangle
; NULLREGION			= 1 Region is empty

SelectObject(hdc, hgdiobj)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("SelectObject", Ptr, hdc, Ptr, hgdiobj)
}

;-------------------------------------------------------------------------------------

; Function				DeleteObject
; Description			This function deletes a logical pen, brush, font, bitmap, region, or palette, freeing all system resources associated with the object
;						After the object is deleted, the specified handle is no longer valid
;
; hObject				Handle to a logical pen, brush, font, bitmap, region, or palette to delete
;
; return				Nonzero indicates success. Zero indicates that the specified handle is not valid or that the handle is currently selected into a device context

DeleteObject(hObject)
{
   return DllCall("DeleteObject", A_PtrSize ? "UPtr" : "UInt", hObject)
}

;-------------------------------------------------------------------------------------

; Function				GetDC
; Description			This function retrieves a handle to a display device context (DC) for the client area of the specified window.
;						The display device context can be used in subsequent graphics display interface (GDI) functions to draw in the client area of the window. 
;
; hwnd					Handle to the window whose device context is to be retrieved. If this value is NULL, GetDC retrieves the device context for the entire screen					
;
; return				The handle the device context for the specified window's client area indicates success. NULL indicates failure

GetDC(hwnd=0)
{
	return DllCall("GetDC", A_PtrSize ? "UPtr" : "UInt", hwnd)
}

;-------------------------------------------------------------------------------------

; DCX_CACHE = 0x2
; DCX_CLIPCHILDREN = 0x8
; DCX_CLIPSIBLINGS = 0x10
; DCX_EXCLUDERGN = 0x40
; DCX_EXCLUDEUPDATE = 0x100
; DCX_INTERSECTRGN = 0x80
; DCX_INTERSECTUPDATE = 0x200
; DCX_LOCKWINDOWUPDATE = 0x400
; DCX_NORECOMPUTE = 0x100000
; DCX_NORESETATTRS = 0x4
; DCX_PARENTCLIP = 0x20
; DCX_VALIDATE = 0x200000
; DCX_WINDOW = 0x1

GetDCEx(hwnd, flags=0, hrgnClip=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
    return DllCall("GetDCEx", Ptr, hwnd, Ptr, hrgnClip, "int", flags)
}

;-------------------------------------------------------------------------------------

; Function				ReleaseDC
; Description			This function releases a device context (DC), freeing it for use by other applications. The effect of ReleaseDC depends on the type of device context
;
; hdc					Handle to the device context to be released
; hwnd					Handle to the window whose device context is to be released
;
; return				1 = released
;						0 = not released
;
; notes					The application must call the ReleaseDC function for each call to the GetWindowDC function and for each call to the GetDC function that retrieves a common device context
;						An application cannot use the ReleaseDC function to release a device context that was created by calling the CreateDC function; instead, it must use the DeleteDC function. 

ReleaseDC(hdc, hwnd=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("ReleaseDC", Ptr, hwnd, Ptr, hdc)
}

;-------------------------------------------------------------------------------------

; Function				DeleteDC
; Description			The DeleteDC function deletes the specified device context (DC)
;
; hdc					A handle to the device context
;
; return				If the function succeeds, the return value is nonzero
;
; notes					An application must not delete a DC whose handle was obtained by calling the GetDC function. Instead, it must call the ReleaseDC function to free the DC

DeleteDC(hdc)
{
   return DllCall("DeleteDC", A_PtrSize ? "UPtr" : "UInt", hdc)
}
;-------------------------------------------------------------------------------------

; Function				Gdip_LibraryVersion
; Description			Get the current library version
;
; return				the library version
;
; notes					This is useful for non compiled programs to ensure that a person doesn't run an old version when testing your scripts

Gdip_LibraryVersion()
{
	return 1.45
}

;-------------------------------------------------------------------------------------

; Function				Gdip_LibrarySubVersion
; Description			Get the current library sub version
;
; return				the library sub version
;
; notes					This is the sub-version currently maintained by Rseding91
Gdip_LibrarySubVersion()
{
	return 1.47
}

;-------------------------------------------------------------------------------------

; Function:    			Gdip_BitmapFromBRA
; Description: 			Gets a pointer to a gdi+ bitmap from a BRA file
;
; BRAFromMemIn			The variable for a BRA file read to memory
; File					The name of the file, or its number that you would like (This depends on alternate parameter)
; Alternate				Changes whether the File parameter is the file name or its number
;
; return      			If the function succeeds, the return value is a pointer to a gdi+ bitmap
;						-1 = The BRA variable is empty
;						-2 = The BRA has an incorrect header
;						-3 = The BRA has information missing
;						-4 = Could not find file inside the BRA

Gdip_BitmapFromBRA(ByRef BRAFromMemIn, File, Alternate=0)
{
	Static FName = "ObjRelease"
	
	if !BRAFromMemIn
		return -1
	Loop, Parse, BRAFromMemIn, `n
	{
		if (A_Index = 1)
		{
			StringSplit, Header, A_LoopField, |
			if (Header0 != 4 || Header2 != "BRA!")
				return -2
		}
		else if (A_Index = 2)
		{
			StringSplit, Info, A_LoopField, |
			if (Info0 != 3)
				return -3
		}
		else
			break
	}
	if !Alternate
		StringReplace, File, File, \, \\, All
	RegExMatch(BRAFromMemIn, "mi`n)^" (Alternate ? File "\|.+?\|(\d+)\|(\d+)" : "\d+\|" File "\|(\d+)\|(\d+)") "$", FileInfo)
	if !FileInfo
		return -4
	
	hData := DllCall("GlobalAlloc", "uint", 2, Ptr, FileInfo2, Ptr)
	pData := DllCall("GlobalLock", Ptr, hData, Ptr)
	DllCall("RtlMoveMemory", Ptr, pData, Ptr, &BRAFromMemIn+Info2+FileInfo1, Ptr, FileInfo2)
	DllCall("GlobalUnlock", Ptr, hData)
	DllCall("ole32\CreateStreamOnHGlobal", Ptr, hData, "int", 1, A_PtrSize ? "UPtr*" : "UInt*", pStream)
	DllCall("gdiplus\GdipCreateBitmapFromStream", Ptr, pStream, A_PtrSize ? "UPtr*" : "UInt*", pBitmap)
	If (A_PtrSize)
		%FName%(pStream)
	Else
		DllCall(NumGet(NumGet(1*pStream)+8), "uint", pStream)
	return pBitmap
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawRectangle
; Description			This function uses a pen to draw the outline of a rectangle into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x						x-coordinate of the top left of the rectangle
; y						y-coordinate of the top left of the rectangle
; w						width of the rectanlge
; h						height of the rectangle
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawRectangle(pGraphics, pPen, x, y, w, h)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawRectangle", Ptr, pGraphics, Ptr, pPen, "float", x, "float", y, "float", w, "float", h)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawRoundedRectangle
; Description			This function uses a pen to draw the outline of a rounded rectangle into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x						x-coordinate of the top left of the rounded rectangle
; y						y-coordinate of the top left of the rounded rectangle
; w						width of the rectanlge
; h						height of the rectangle
; r						radius of the rounded corners
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawRoundedRectangle(pGraphics, pPen, x, y, w, h, r)
{
	Gdip_SetClipRect(pGraphics, x-r, y-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x+w-r, y-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x-r, y+h-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x+w-r, y+h-r, 2*r, 2*r, 4)
	E := Gdip_DrawRectangle(pGraphics, pPen, x, y, w, h)
	Gdip_ResetClip(pGraphics)
	Gdip_SetClipRect(pGraphics, x-(2*r), y+r, w+(4*r), h-(2*r), 4)
	Gdip_SetClipRect(pGraphics, x+r, y-(2*r), w-(2*r), h+(4*r), 4)
	Gdip_DrawEllipse(pGraphics, pPen, x, y, 2*r, 2*r)
	Gdip_DrawEllipse(pGraphics, pPen, x+w-(2*r), y, 2*r, 2*r)
	Gdip_DrawEllipse(pGraphics, pPen, x, y+h-(2*r), 2*r, 2*r)
	Gdip_DrawEllipse(pGraphics, pPen, x+w-(2*r), y+h-(2*r), 2*r, 2*r)
	Gdip_ResetClip(pGraphics)
	return E
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawEllipse
; Description			This function uses a pen to draw the outline of an ellipse into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x						x-coordinate of the top left of the rectangle the ellipse will be drawn into
; y						y-coordinate of the top left of the rectangle the ellipse will be drawn into
; w						width of the ellipse
; h						height of the ellipse
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawEllipse(pGraphics, pPen, x, y, w, h)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawEllipse", Ptr, pGraphics, Ptr, pPen, "float", x, "float", y, "float", w, "float", h)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawBezier
; Description			This function uses a pen to draw the outline of a bezier (a weighted curve) into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x1					x-coordinate of the start of the bezier
; y1					y-coordinate of the start of the bezier
; x2					x-coordinate of the first arc of the bezier
; y2					y-coordinate of the first arc of the bezier
; x3					x-coordinate of the second arc of the bezier
; y3					y-coordinate of the second arc of the bezier
; x4					x-coordinate of the end of the bezier
; y4					y-coordinate of the end of the bezier
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawBezier(pGraphics, pPen, x1, y1, x2, y2, x3, y3, x4, y4)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawBezier"
					, Ptr, pgraphics
					, Ptr, pPen
					, "float", x1
					, "float", y1
					, "float", x2
					, "float", y2
					, "float", x3
					, "float", y3
					, "float", x4
					, "float", y4)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawArc
; Description			This function uses a pen to draw the outline of an arc into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x						x-coordinate of the start of the arc
; y						y-coordinate of the start of the arc
; w						width of the arc
; h						height of the arc
; StartAngle			specifies the angle between the x-axis and the starting point of the arc
; SweepAngle			specifies the angle between the starting and ending points of the arc
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawArc(pGraphics, pPen, x, y, w, h, StartAngle, SweepAngle)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawArc"
					, Ptr, pGraphics
					, Ptr, pPen
					, "float", x
					, "float", y
					, "float", w
					, "float", h
					, "float", StartAngle
					, "float", SweepAngle)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawPie
; Description			This function uses a pen to draw the outline of a pie into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x						x-coordinate of the start of the pie
; y						y-coordinate of the start of the pie
; w						width of the pie
; h						height of the pie
; StartAngle			specifies the angle between the x-axis and the starting point of the pie
; SweepAngle			specifies the angle between the starting and ending points of the pie
;
; return				status enumeration. 0 = success
;
; notes					as all coordinates are taken from the top left of each pixel, then the entire width/height should be specified as subtracting the pen width

Gdip_DrawPie(pGraphics, pPen, x, y, w, h, StartAngle, SweepAngle)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawPie", Ptr, pGraphics, Ptr, pPen, "float", x, "float", y, "float", w, "float", h, "float", StartAngle, "float", SweepAngle)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawLine
; Description			This function uses a pen to draw a line into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; x1					x-coordinate of the start of the line
; y1					y-coordinate of the start of the line
; x2					x-coordinate of the end of the line
; y2					y-coordinate of the end of the line
;
; return				status enumeration. 0 = success		

Gdip_DrawLine(pGraphics, pPen, x1, y1, x2, y2)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipDrawLine"
					, Ptr, pGraphics
					, Ptr, pPen
					, "float", x1
					, "float", y1
					, "float", x2
					, "float", y2)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawLines
; Description			This function uses a pen to draw a series of joined lines into the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pPen					Pointer to a pen
; Points				the coordinates of all the points passed as x1,y1|x2,y2|x3,y3.....
;
; return				status enumeration. 0 = success				

Gdip_DrawLines(pGraphics, pPen, Points)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	StringSplit, Points, Points, |
	VarSetCapacity(PointF, 8*Points0)   
	Loop, %Points0%
	{
		StringSplit, Coord, Points%A_Index%, `,
		NumPut(Coord1, PointF, 8*(A_Index-1), "float"), NumPut(Coord2, PointF, (8*(A_Index-1))+4, "float")
	}
	return DllCall("gdiplus\GdipDrawLines", Ptr, pGraphics, Ptr, pPen, Ptr, &PointF, "int", Points0)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillRectangle
; Description			This function uses a brush to fill a rectangle in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; x						x-coordinate of the top left of the rectangle
; y						y-coordinate of the top left of the rectangle
; w						width of the rectanlge
; h						height of the rectangle
;
; return				status enumeration. 0 = success

Gdip_FillRectangle(pGraphics, pBrush, x, y, w, h)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipFillRectangle"
					, Ptr, pGraphics
					, Ptr, pBrush
					, "float", x
					, "float", y
					, "float", w
					, "float", h)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillRoundedRectangle
; Description			This function uses a brush to fill a rounded rectangle in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; x						x-coordinate of the top left of the rounded rectangle
; y						y-coordinate of the top left of the rounded rectangle
; w						width of the rectanlge
; h						height of the rectangle
; r						radius of the rounded corners
;
; return				status enumeration. 0 = success

Gdip_FillRoundedRectangle(pGraphics, pBrush, x, y, w, h, r)
{
	Region := Gdip_GetClipRegion(pGraphics)
	Gdip_SetClipRect(pGraphics, x-r, y-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x+w-r, y-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x-r, y+h-r, 2*r, 2*r, 4)
	Gdip_SetClipRect(pGraphics, x+w-r, y+h-r, 2*r, 2*r, 4)
	E := Gdip_FillRectangle(pGraphics, pBrush, x, y, w, h)
	Gdip_SetClipRegion(pGraphics, Region, 0)
	Gdip_SetClipRect(pGraphics, x-(2*r), y+r, w+(4*r), h-(2*r), 4)
	Gdip_SetClipRect(pGraphics, x+r, y-(2*r), w-(2*r), h+(4*r), 4)
	Gdip_FillEllipse(pGraphics, pBrush, x, y, 2*r, 2*r)
	Gdip_FillEllipse(pGraphics, pBrush, x+w-(2*r), y, 2*r, 2*r)
	Gdip_FillEllipse(pGraphics, pBrush, x, y+h-(2*r), 2*r, 2*r)
	Gdip_FillEllipse(pGraphics, pBrush, x+w-(2*r), y+h-(2*r), 2*r, 2*r)
	Gdip_SetClipRegion(pGraphics, Region, 0)
	Gdip_DeleteRegion(Region)
	return E
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillPolygon
; Description			This function uses a brush to fill a polygon in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; Points				the coordinates of all the points passed as x1,y1|x2,y2|x3,y3.....
;
; return				status enumeration. 0 = success
;
; notes					Alternate will fill the polygon as a whole, wheras winding will fill each new "segment"
; Alternate 			= 0
; Winding 				= 1

Gdip_FillPolygon(pGraphics, pBrush, Points, FillMode=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	StringSplit, Points, Points, |
	VarSetCapacity(PointF, 8*Points0)   
	Loop, %Points0%
	{
		StringSplit, Coord, Points%A_Index%, `,
		NumPut(Coord1, PointF, 8*(A_Index-1), "float"), NumPut(Coord2, PointF, (8*(A_Index-1))+4, "float")
	}   
	return DllCall("gdiplus\GdipFillPolygon", Ptr, pGraphics, Ptr, pBrush, Ptr, &PointF, "int", Points0, "int", FillMode)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillPie
; Description			This function uses a brush to fill a pie in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; x						x-coordinate of the top left of the pie
; y						y-coordinate of the top left of the pie
; w						width of the pie
; h						height of the pie
; StartAngle			specifies the angle between the x-axis and the starting point of the pie
; SweepAngle			specifies the angle between the starting and ending points of the pie
;
; return				status enumeration. 0 = success

Gdip_FillPie(pGraphics, pBrush, x, y, w, h, StartAngle, SweepAngle)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipFillPie"
					, Ptr, pGraphics
					, Ptr, pBrush
					, "float", x
					, "float", y
					, "float", w
					, "float", h
					, "float", StartAngle
					, "float", SweepAngle)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillEllipse
; Description			This function uses a brush to fill an ellipse in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; x						x-coordinate of the top left of the ellipse
; y						y-coordinate of the top left of the ellipse
; w						width of the ellipse
; h						height of the ellipse
;
; return				status enumeration. 0 = success

Gdip_FillEllipse(pGraphics, pBrush, x, y, w, h)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipFillEllipse", Ptr, pGraphics, Ptr, pBrush, "float", x, "float", y, "float", w, "float", h)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillRegion
; Description			This function uses a brush to fill a region in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; Region				Pointer to a Region
;
; return				status enumeration. 0 = success
;
; notes					You can create a region Gdip_CreateRegion() and then add to this

Gdip_FillRegion(pGraphics, pBrush, Region)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipFillRegion", Ptr, pGraphics, Ptr, pBrush, Ptr, Region)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_FillPath
; Description			This function uses a brush to fill a path in the Graphics of a bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBrush				Pointer to a brush
; Region				Pointer to a Path
;
; return				status enumeration. 0 = success

Gdip_FillPath(pGraphics, pBrush, Path)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipFillPath", Ptr, pGraphics, Ptr, pBrush, Ptr, Path)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawImagePointsRect
; Description			This function draws a bitmap into the Graphics of another bitmap and skews it
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBitmap				Pointer to a bitmap to be drawn
; Points				Points passed as x1,y1|x2,y2|x3,y3 (3 points: top left, top right, bottom left) describing the drawing of the bitmap
; sx					x-coordinate of source upper-left corner
; sy					y-coordinate of source upper-left corner
; sw					width of source rectangle
; sh					height of source rectangle
; Matrix				a matrix used to alter image attributes when drawing
;
; return				status enumeration. 0 = success
;
; notes					if sx,sy,sw,sh are missed then the entire source bitmap will be used
;						Matrix can be omitted to just draw with no alteration to ARGB
;						Matrix may be passed as a digit from 0 - 1 to change just transparency
;						Matrix can be passed as a matrix with any delimiter

Gdip_DrawImagePointsRect(pGraphics, pBitmap, Points, sx="", sy="", sw="", sh="", Matrix=1)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	StringSplit, Points, Points, |
	VarSetCapacity(PointF, 8*Points0)   
	Loop, %Points0%
	{
		StringSplit, Coord, Points%A_Index%, `,
		NumPut(Coord1, PointF, 8*(A_Index-1), "float"), NumPut(Coord2, PointF, (8*(A_Index-1))+4, "float")
	}

	if (Matrix&1 = "")
		ImageAttr := Gdip_SetImageAttributesColorMatrix(Matrix)
	else if (Matrix != 1)
		ImageAttr := Gdip_SetImageAttributesColorMatrix("1|0|0|0|0|0|1|0|0|0|0|0|1|0|0|0|0|0|" Matrix "|0|0|0|0|0|1")
		
	if (sx = "" && sy = "" && sw = "" && sh = "")
	{
		sx := 0, sy := 0
		sw := Gdip_GetImageWidth(pBitmap)
		sh := Gdip_GetImageHeight(pBitmap)
	}

	E := DllCall("gdiplus\GdipDrawImagePointsRect"
				, Ptr, pGraphics
				, Ptr, pBitmap
				, Ptr, &PointF
				, "int", Points0
				, "float", sx
				, "float", sy
				, "float", sw
				, "float", sh
				, "int", 2
				, Ptr, ImageAttr
				, Ptr, 0
				, Ptr, 0)
	if ImageAttr
		Gdip_DisposeImageAttributes(ImageAttr)
	return E
}

;-------------------------------------------------------------------------------------

; Function				Gdip_DrawImage
; Description			This function draws a bitmap into the Graphics of another bitmap
;
; pGraphics				Pointer to the Graphics of a bitmap
; pBitmap				Pointer to a bitmap to be drawn
; dx					x-coord of destination upper-left corner
; dy					y-coord of destination upper-left corner
; dw					width of destination image
; dh					height of destination image
; sx					x-coordinate of source upper-left corner
; sy					y-coordinate of source upper-left corner
; sw					width of source image
; sh					height of source image
; Matrix				a matrix used to alter image attributes when drawing
;
; return				status enumeration. 0 = success
;
; notes					if sx,sy,sw,sh are missed then the entire source bitmap will be used
;						Gdip_DrawImage performs faster
;						Matrix can be omitted to just draw with no alteration to ARGB
;						Matrix may be passed as a digit from 0 - 1 to change just transparency
;						Matrix can be passed as a matrix with any delimiter. For example:
;						MatrixBright=
;						(
;						1.5		|0		|0		|0		|0
;						0		|1.5	|0		|0		|0
;						0		|0		|1.5	|0		|0
;						0		|0		|0		|1		|0
;						0.05	|0.05	|0.05	|0		|1
;						)
;
; notes					MatrixBright = 1.5|0|0|0|0|0|1.5|0|0|0|0|0|1.5|0|0|0|0|0|1|0|0.05|0.05|0.05|0|1
;						MatrixGreyScale = 0.299|0.299|0.299|0|0|0.587|0.587|0.587|0|0|0.114|0.114|0.114|0|0|0|0|0|1|0|0|0|0|0|1
;						MatrixNegative = -1|0|0|0|0|0|-1|0|0|0|0|0|-1|0|0|0|0|0|1|0|0|0|0|0|1

Gdip_DrawImage(pGraphics, pBitmap, dx="", dy="", dw="", dh="", sx="", sy="", sw="", sh="", Matrix=1)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if (Matrix&1 = "")
		ImageAttr := Gdip_SetImageAttributesColorMatrix(Matrix)
	else if (Matrix != 1)
		ImageAttr := Gdip_SetImageAttributesColorMatrix("1|0|0|0|0|0|1|0|0|0|0|0|1|0|0|0|0|0|" Matrix "|0|0|0|0|0|1")

	if (sx = "" && sy = "" && sw = "" && sh = "")
	{
		if (dx = "" && dy = "" && dw = "" && dh = "")
		{
			sx := dx := 0, sy := dy := 0
			sw := dw := Gdip_GetImageWidth(pBitmap)
			sh := dh := Gdip_GetImageHeight(pBitmap)
		}
		else
		{
			sx := sy := 0
			sw := Gdip_GetImageWidth(pBitmap)
			sh := Gdip_GetImageHeight(pBitmap)
		}
	}

	E := DllCall("gdiplus\GdipDrawImageRectRect"
				, Ptr, pGraphics
				, Ptr, pBitmap
				, "float", dx
				, "float", dy
				, "float", dw
				, "float", dh
				, "float", sx
				, "float", sy
				, "float", sw
				, "float", sh
				, "int", 2
				, Ptr, ImageAttr
				, Ptr, 0
				, Ptr, 0)
	if ImageAttr
		Gdip_DisposeImageAttributes(ImageAttr)
	return E
}

;-------------------------------------------------------------------------------------

; Function				Gdip_SetImageAttributesColorMatrix
; Description			This function creates an image matrix ready for drawing
;
; Matrix				a matrix used to alter image attributes when drawing
;						passed with any delimeter
;
; return				returns an image matrix on sucess or 0 if it fails
;
; notes					MatrixBright = 1.5|0|0|0|0|0|1.5|0|0|0|0|0|1.5|0|0|0|0|0|1|0|0.05|0.05|0.05|0|1
;						MatrixGreyScale = 0.299|0.299|0.299|0|0|0.587|0.587|0.587|0|0|0.114|0.114|0.114|0|0|0|0|0|1|0|0|0|0|0|1
;						MatrixNegative = -1|0|0|0|0|0|-1|0|0|0|0|0|-1|0|0|0|0|0|1|0|0|0|0|0|1

Gdip_SetImageAttributesColorMatrix(Matrix)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	VarSetCapacity(ColourMatrix, 100, 0)
	Matrix := RegExReplace(RegExReplace(Matrix, "^[^\d-\.]+([\d\.])", "$1", "", 1), "[^\d-\.]+", "|")
	StringSplit, Matrix, Matrix, |
	Loop, 25
	{
		Matrix := (Matrix%A_Index% != "") ? Matrix%A_Index% : Mod(A_Index-1, 6) ? 0 : 1
		NumPut(Matrix, ColourMatrix, (A_Index-1)*4, "float")
	}
	DllCall("gdiplus\GdipCreateImageAttributes", A_PtrSize ? "UPtr*" : "uint*", ImageAttr)
	DllCall("gdiplus\GdipSetImageAttributesColorMatrix", Ptr, ImageAttr, "int", 1, "int", 1, Ptr, &ColourMatrix, Ptr, 0, "int", 0)
	return ImageAttr
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GraphicsFromImage
; Description			This function gets the graphics for a bitmap used for drawing functions
;
; pBitmap				Pointer to a bitmap to get the pointer to its graphics
;
; return				returns a pointer to the graphics of a bitmap
;
; notes					a bitmap can be drawn into the graphics of another bitmap

Gdip_GraphicsFromImage(pBitmap)
{
	DllCall("gdiplus\GdipGetImageGraphicsContext", A_PtrSize ? "UPtr" : "UInt", pBitmap, A_PtrSize ? "UPtr*" : "UInt*", pGraphics)
	return pGraphics
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GraphicsFromHDC
; Description			This function gets the graphics from the handle to a device context
;
; hdc					This is the handle to the device context
;
; return				returns a pointer to the graphics of a bitmap
;
; notes					You can draw a bitmap into the graphics of another bitmap

Gdip_GraphicsFromHDC(hdc)
{
    DllCall("gdiplus\GdipCreateFromHDC", A_PtrSize ? "UPtr" : "UInt", hdc, A_PtrSize ? "UPtr*" : "UInt*", pGraphics)
    return pGraphics
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetDC
; Description			This function gets the device context of the passed Graphics
;
; hdc					This is the handle to the device context
;
; return				returns the device context for the graphics of a bitmap

Gdip_GetDC(pGraphics)
{
	DllCall("gdiplus\GdipGetDC", A_PtrSize ? "UPtr" : "UInt", pGraphics, A_PtrSize ? "UPtr*" : "UInt*", hdc)
	return hdc
}

;-------------------------------------------------------------------------------------

; Function				Gdip_ReleaseDC
; Description			This function releases a device context from use for further use
;
; pGraphics				Pointer to the graphics of a bitmap
; hdc					This is the handle to the device context
;
; return				status enumeration. 0 = success

Gdip_ReleaseDC(pGraphics, hdc)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipReleaseDC", Ptr, pGraphics, Ptr, hdc)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GraphicsClear
; Description			Clears the graphics of a bitmap ready for further drawing
;
; pGraphics				Pointer to the graphics of a bitmap
; ARGB					The colour to clear the graphics to
;
; return				status enumeration. 0 = success
;
; notes					By default this will make the background invisible
;						Using clipping regions you can clear a particular area on the graphics rather than clearing the entire graphics

Gdip_GraphicsClear(pGraphics, ARGB=0x00ffffff)
{
    return DllCall("gdiplus\GdipGraphicsClear", A_PtrSize ? "UPtr" : "UInt", pGraphics, "int", ARGB)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_BlurBitmap
; Description			Gives a pointer to a blurred bitmap from a pointer to a bitmap
;
; pBitmap				Pointer to a bitmap to be blurred
; Blur					The Amount to blur a bitmap by from 1 (least blur) to 100 (most blur)
;
; return				If the function succeeds, the return value is a pointer to the new blurred bitmap
;						-1 = The blur parameter is outside the range 1-100
;
; notes					This function will not dispose of the original bitmap

Gdip_BlurBitmap(pBitmap, Blur)
{
	if (Blur > 100) || (Blur < 1)
		return -1	
	
	sWidth := Gdip_GetImageWidth(pBitmap), sHeight := Gdip_GetImageHeight(pBitmap)
	dWidth := sWidth//Blur, dHeight := sHeight//Blur

	pBitmap1 := Gdip_CreateBitmap(dWidth, dHeight)
	G1 := Gdip_GraphicsFromImage(pBitmap1)
	Gdip_SetInterpolationMode(G1, 7)
	Gdip_DrawImage(G1, pBitmap, 0, 0, dWidth, dHeight, 0, 0, sWidth, sHeight)

	Gdip_DeleteGraphics(G1)

	pBitmap2 := Gdip_CreateBitmap(sWidth, sHeight)
	G2 := Gdip_GraphicsFromImage(pBitmap2)
	Gdip_SetInterpolationMode(G2, 7)
	Gdip_DrawImage(G2, pBitmap1, 0, 0, sWidth, sHeight, 0, 0, dWidth, dHeight)

	Gdip_DeleteGraphics(G2)
	Gdip_DisposeImage(pBitmap1)
	return pBitmap2
}

;-------------------------------------------------------------------------------------

; Function:     		Gdip_SaveBitmapToFile
; Description:  		Saves a bitmap to a file in any supported format onto disk
;   
; pBitmap				Pointer to a bitmap
; sOutput      			The name of the file that the bitmap will be saved to. Supported extensions are: .BMP,.DIB,.RLE,.JPG,.JPEG,.JPE,.JFIF,.GIF,.TIF,.TIFF,.PNG
; Quality      			If saving as jpg (.JPG,.JPEG,.JPE,.JFIF) then quality can be 1-100 with default at maximum quality
;
; return      			If the function succeeds, the return value is zero, otherwise:
;						-1 = Extension supplied is not a supported file format
;						-2 = Could not get a list of encoders on system
;						-3 = Could not find matching encoder for specified file format
;						-4 = Could not get WideChar name of output file
;						-5 = Could not save file to disk
;
; notes					This function will use the extension supplied from the sOutput parameter to determine the output format

Gdip_SaveBitmapToFile(pBitmap, sOutput, Quality=75)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	SplitPath, sOutput,,, Extension
	if Extension not in BMP,DIB,RLE,JPG,JPEG,JPE,JFIF,GIF,TIF,TIFF,PNG
		return -1
	Extension := "." Extension

	DllCall("gdiplus\GdipGetImageEncodersSize", "uint*", nCount, "uint*", nSize)
	VarSetCapacity(ci, nSize)
	DllCall("gdiplus\GdipGetImageEncoders", "uint", nCount, "uint", nSize, Ptr, &ci)
	if !(nCount && nSize)
		return -2
	
	If (A_IsUnicode){
		StrGet_Name := "StrGet"
		Loop, %nCount%
		{
			sString := %StrGet_Name%(NumGet(ci, (idx := (48+7*A_PtrSize)*(A_Index-1))+32+3*A_PtrSize), "UTF-16")
			if !InStr(sString, "*" Extension)
				continue
			
			pCodec := &ci+idx
			break
		}
	} else {
		Loop, %nCount%
		{
			Location := NumGet(ci, 76*(A_Index-1)+44)
			nSize := DllCall("WideCharToMultiByte", "uint", 0, "uint", 0, "uint", Location, "int", -1, "uint", 0, "int",  0, "uint", 0, "uint", 0)
			VarSetCapacity(sString, nSize)
			DllCall("WideCharToMultiByte", "uint", 0, "uint", 0, "uint", Location, "int", -1, "str", sString, "int", nSize, "uint", 0, "uint", 0)
			if !InStr(sString, "*" Extension)
				continue
			
			pCodec := &ci+76*(A_Index-1)
			break
		}
	}
	
	if !pCodec
		return -3

	if (Quality != 75)
	{
		Quality := (Quality < 0) ? 0 : (Quality > 100) ? 100 : Quality
		if Extension in .JPG,.JPEG,.JPE,.JFIF
		{
			DllCall("gdiplus\GdipGetEncoderParameterListSize", Ptr, pBitmap, Ptr, pCodec, "uint*", nSize)
			VarSetCapacity(EncoderParameters, nSize, 0)
			DllCall("gdiplus\GdipGetEncoderParameterList", Ptr, pBitmap, Ptr, pCodec, "uint", nSize, Ptr, &EncoderParameters)
			Loop, % NumGet(EncoderParameters, "UInt")      ;%
			{
				elem := (24+(A_PtrSize ? A_PtrSize : 4))*(A_Index-1) + 4 + (pad := A_PtrSize = 8 ? 4 : 0)
				if (NumGet(EncoderParameters, elem+16, "UInt") = 1) && (NumGet(EncoderParameters, elem+20, "UInt") = 6)
				{
					p := elem+&EncoderParameters-pad-4
					NumPut(Quality, NumGet(NumPut(4, NumPut(1, p+0)+20, "UInt")), "UInt")
					break
				}
			}      
		}
	}

	if (!A_IsUnicode)
	{
		nSize := DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sOutput, "int", -1, Ptr, 0, "int", 0)
		VarSetCapacity(wOutput, nSize*2)
		DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sOutput, "int", -1, Ptr, &wOutput, "int", nSize)
		VarSetCapacity(wOutput, -1)
		if !VarSetCapacity(wOutput)
			return -4
		E := DllCall("gdiplus\GdipSaveImageToFile", Ptr, pBitmap, Ptr, &wOutput, Ptr, pCodec, "uint", p ? p : 0)
	}
	else
		E := DllCall("gdiplus\GdipSaveImageToFile", Ptr, pBitmap, Ptr, &sOutput, Ptr, pCodec, "uint", p ? p : 0)
	return E ? -5 : 0
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetPixel
; Description			Gets the ARGB of a pixel in a bitmap
;
; pBitmap				Pointer to a bitmap
; x						x-coordinate of the pixel
; y						y-coordinate of the pixel
;
; return				Returns the ARGB value of the pixel

Gdip_GetPixel(pBitmap, x, y)
{
	DllCall("gdiplus\GdipBitmapGetPixel", A_PtrSize ? "UPtr" : "UInt", pBitmap, "int", x, "int", y, "uint*", ARGB)
	return ARGB
}

;-------------------------------------------------------------------------------------

; Function				Gdip_SetPixel
; Description			Sets the ARGB of a pixel in a bitmap
;
; pBitmap				Pointer to a bitmap
; x						x-coordinate of the pixel
; y						y-coordinate of the pixel
;
; return				status enumeration. 0 = success

Gdip_SetPixel(pBitmap, x, y, ARGB)
{
   return DllCall("gdiplus\GdipBitmapSetPixel", A_PtrSize ? "UPtr" : "UInt", pBitmap, "int", x, "int", y, "int", ARGB)
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetImageWidth
; Description			Gives the width of a bitmap
;
; pBitmap				Pointer to a bitmap
;
; return				Returns the width in pixels of the supplied bitmap

Gdip_GetImageWidth(pBitmap)
{
   DllCall("gdiplus\GdipGetImageWidth", A_PtrSize ? "UPtr" : "UInt", pBitmap, "uint*", Width)
   return Width
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetImageHeight
; Description			Gives the height of a bitmap
;
; pBitmap				Pointer to a bitmap
;
; return				Returns the height in pixels of the supplied bitmap

Gdip_GetImageHeight(pBitmap)
{
   DllCall("gdiplus\GdipGetImageHeight", A_PtrSize ? "UPtr" : "UInt", pBitmap, "uint*", Height)
   return Height
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetDimensions
; Description			Gives the width and height of a bitmap
;
; pBitmap				Pointer to a bitmap
; Width					ByRef variable. This variable will be set to the width of the bitmap
; Height				ByRef variable. This variable will be set to the height of the bitmap
;
; return				No return value
;						Gdip_GetDimensions(pBitmap, ThisWidth, ThisHeight) will set ThisWidth to the width and ThisHeight to the height

Gdip_GetImageDimensions(pBitmap, ByRef Width, ByRef Height)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	DllCall("gdiplus\GdipGetImageWidth", Ptr, pBitmap, "uint*", Width)
	DllCall("gdiplus\GdipGetImageHeight", Ptr, pBitmap, "uint*", Height)
}

;-------------------------------------------------------------------------------------

Gdip_GetDimensions(pBitmap, ByRef Width, ByRef Height)
{
	Gdip_GetImageDimensions(pBitmap, Width, Height)
}

;-------------------------------------------------------------------------------------

Gdip_GetImagePixelFormat(pBitmap)
{
	DllCall("gdiplus\GdipGetImagePixelFormat", A_PtrSize ? "UPtr" : "UInt", pBitmap, A_PtrSize ? "UPtr*" : "UInt*", Format)
	return Format
}

;-------------------------------------------------------------------------------------

; Function				Gdip_GetDpiX
; Description			Gives the horizontal dots per inch of the graphics of a bitmap
;
; pBitmap				Pointer to a bitmap
; Width					ByRef variable. This variable will be set to the width of the bitmap
; Height				ByRef variable. This variable will be set to the height of the bitmap
;
; return				No return value
;						Gdip_GetDimensions(pBitmap, ThisWidth, ThisHeight) will set ThisWidth to the width and ThisHeight to the height

Gdip_GetDpiX(pGraphics)
{
	DllCall("gdiplus\GdipGetDpiX", A_PtrSize ? "UPtr" : "uint", pGraphics, "float*", dpix)
	return Round(dpix)
}

;-------------------------------------------------------------------------------------

Gdip_GetDpiY(pGraphics)
{
	DllCall("gdiplus\GdipGetDpiY", A_PtrSize ? "UPtr" : "uint", pGraphics, "float*", dpiy)
	return Round(dpiy)
}

;-------------------------------------------------------------------------------------

Gdip_GetImageHorizontalResolution(pBitmap)
{
	DllCall("gdiplus\GdipGetImageHorizontalResolution", A_PtrSize ? "UPtr" : "uint", pBitmap, "float*", dpix)
	return Round(dpix)
}

;-------------------------------------------------------------------------------------

Gdip_GetImageVerticalResolution(pBitmap)
{
	DllCall("gdiplus\GdipGetImageVerticalResolution", A_PtrSize ? "UPtr" : "uint", pBitmap, "float*", dpiy)
	return Round(dpiy)
}

;-------------------------------------------------------------------------------------

Gdip_BitmapSetResolution(pBitmap, dpix, dpiy)
{
	return DllCall("gdiplus\GdipBitmapSetResolution", A_PtrSize ? "UPtr" : "uint", pBitmap, "float", dpix, "float", dpiy)
}

;-------------------------------------------------------------------------------------

Gdip_CreateBitmapFromFile(sFile, IconNumber=1, IconSize="")
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	, PtrA := A_PtrSize ? "UPtr*" : "UInt*"
	
	SplitPath, sFile,,, ext
	if ext in exe,dll
	{
		Sizes := IconSize ? IconSize : 256 "|" 128 "|" 64 "|" 48 "|" 32 "|" 16
		BufSize := 16 + (2*(A_PtrSize ? A_PtrSize : 4))
		
		VarSetCapacity(buf, BufSize, 0)
		Loop, Parse, Sizes, |
		{
			DllCall("PrivateExtractIcons", "str", sFile, "int", IconNumber-1, "int", A_LoopField, "int", A_LoopField, PtrA, hIcon, PtrA, 0, "uint", 1, "uint", 0)
			
			if !hIcon
				continue

			if !DllCall("GetIconInfo", Ptr, hIcon, Ptr, &buf)
			{
				DestroyIcon(hIcon)
				continue
			}
			
			hbmMask  := NumGet(buf, 12 + ((A_PtrSize ? A_PtrSize : 4) - 4))
			hbmColor := NumGet(buf, 12 + ((A_PtrSize ? A_PtrSize : 4) - 4) + (A_PtrSize ? A_PtrSize : 4))
			if !(hbmColor && DllCall("GetObject", Ptr, hbmColor, "int", BufSize, Ptr, &buf))
			{
				DestroyIcon(hIcon)
				continue
			}
			break
		}
		if !hIcon
			return -1

		Width := NumGet(buf, 4, "int"), Height := NumGet(buf, 8, "int")
		hbm := CreateDIBSection(Width, -Height), hdc := CreateCompatibleDC(), obm := SelectObject(hdc, hbm)
		if !DllCall("DrawIconEx", Ptr, hdc, "int", 0, "int", 0, Ptr, hIcon, "uint", Width, "uint", Height, "uint", 0, Ptr, 0, "uint", 3)
		{
			DestroyIcon(hIcon)
			return -2
		}
		
		VarSetCapacity(dib, 104)
		DllCall("GetObject", Ptr, hbm, "int", A_PtrSize = 8 ? 104 : 84, Ptr, &dib) ; sizeof(DIBSECTION) = 76+2*(A_PtrSize=8?4:0)+2*A_PtrSize
		Stride := NumGet(dib, 12, "Int"), Bits := NumGet(dib, 20 + (A_PtrSize = 8 ? 4 : 0)) ; padding
		DllCall("gdiplus\GdipCreateBitmapFromScan0", "int", Width, "int", Height, "int", Stride, "int", 0x26200A, Ptr, Bits, PtrA, pBitmapOld)
		pBitmap := Gdip_CreateBitmap(Width, Height)
		G := Gdip_GraphicsFromImage(pBitmap)
		, Gdip_DrawImage(G, pBitmapOld, 0, 0, Width, Height, 0, 0, Width, Height)
		SelectObject(hdc, obm), DeleteObject(hbm), DeleteDC(hdc)
		Gdip_DeleteGraphics(G), Gdip_DisposeImage(pBitmapOld)
		DestroyIcon(hIcon)
	}
	else
	{
		if (!A_IsUnicode)
		{
			VarSetCapacity(wFile, 1024)
			DllCall("kernel32\MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sFile, "int", -1, Ptr, &wFile, "int", 512)
			DllCall("gdiplus\GdipCreateBitmapFromFile", Ptr, &wFile, PtrA, pBitmap)
		}
		else
			DllCall("gdiplus\GdipCreateBitmapFromFile", Ptr, &sFile, PtrA, pBitmap)
	}
	
	return pBitmap
}

;-------------------------------------------------------------------------------------

Gdip_CreateBitmapFromHBITMAP(hBitmap, Palette=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	DllCall("gdiplus\GdipCreateBitmapFromHBITMAP", Ptr, hBitmap, Ptr, Palette, A_PtrSize ? "UPtr*" : "uint*", pBitmap)
	return pBitmap
}

;-------------------------------------------------------------------------------------

Gdip_CreateHBITMAPFromBitmap(pBitmap, Background=0xffffffff)
{
	DllCall("gdiplus\GdipCreateHBITMAPFromBitmap", A_PtrSize ? "UPtr" : "UInt", pBitmap, A_PtrSize ? "UPtr*" : "uint*", hbm, "int", Background)
	return hbm
}

;-------------------------------------------------------------------------------------

Gdip_CreateBitmapFromHICON(hIcon)
{
	DllCall("gdiplus\GdipCreateBitmapFromHICON", A_PtrSize ? "UPtr" : "UInt", hIcon, A_PtrSize ? "UPtr*" : "uint*", pBitmap)
	return pBitmap
}

;-------------------------------------------------------------------------------------

Gdip_CreateHICONFromBitmap(pBitmap)
{
	DllCall("gdiplus\GdipCreateHICONFromBitmap", A_PtrSize ? "UPtr" : "UInt", pBitmap, A_PtrSize ? "UPtr*" : "uint*", hIcon)
	return hIcon
}

;-------------------------------------------------------------------------------------

Gdip_CreateBitmap(Width, Height, Format=0x26200A)
{
    DllCall("gdiplus\GdipCreateBitmapFromScan0", "int", Width, "int", Height, "int", 0, "int", Format, A_PtrSize ? "UPtr" : "UInt", 0, A_PtrSize ? "UPtr*" : "uint*", pBitmap)
    Return pBitmap
}

;-------------------------------------------------------------------------------------

Gdip_CreateBitmapFromClipboard()
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if !DllCall("OpenClipboard", Ptr, 0)
		return -1
	if !DllCall("IsClipboardFormatAvailable", "uint", 8)
		return -2
	if !hBitmap := DllCall("GetClipboardData", "uint", 2, Ptr)
		return -3
	if !pBitmap := Gdip_CreateBitmapFromHBITMAP(hBitmap)
		return -4
	if !DllCall("CloseClipboard")
		return -5
	DeleteObject(hBitmap)
	return pBitmap
}

;-------------------------------------------------------------------------------------

Gdip_SetBitmapToClipboard(pBitmap)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	off1 := A_PtrSize = 8 ? 52 : 44, off2 := A_PtrSize = 8 ? 32 : 24
	hBitmap := Gdip_CreateHBITMAPFromBitmap(pBitmap)
	DllCall("GetObject", Ptr, hBitmap, "int", VarSetCapacity(oi, A_PtrSize = 8 ? 104 : 84, 0), Ptr, &oi)
	hdib := DllCall("GlobalAlloc", "uint", 2, Ptr, 40+NumGet(oi, off1, "UInt"), Ptr)
	pdib := DllCall("GlobalLock", Ptr, hdib, Ptr)
	DllCall("RtlMoveMemory", Ptr, pdib, Ptr, &oi+off2, Ptr, 40)
	DllCall("RtlMoveMemory", Ptr, pdib+40, Ptr, NumGet(oi, off2 - (A_PtrSize ? A_PtrSize : 4), Ptr), Ptr, NumGet(oi, off1, "UInt"))
	DllCall("GlobalUnlock", Ptr, hdib)
	DllCall("DeleteObject", Ptr, hBitmap)
	DllCall("OpenClipboard", Ptr, 0)
	DllCall("EmptyClipboard")
	DllCall("SetClipboardData", "uint", 8, Ptr, hdib)
	DllCall("CloseClipboard")
}

;-------------------------------------------------------------------------------------

Gdip_CloneBitmapArea(pBitmap, x, y, w, h, Format=0x26200A)
{
	DllCall("gdiplus\GdipCloneBitmapArea"
					, "float", x
					, "float", y
					, "float", w
					, "float", h
					, "int", Format
					, A_PtrSize ? "UPtr" : "UInt", pBitmap
					, A_PtrSize ? "UPtr*" : "UInt*", pBitmapDest)
	return pBitmapDest
}

;-------------------------------------------------------------------------------------
; Create resources
;-------------------------------------------------------------------------------------

Gdip_CreatePen(ARGB, w)
{
   DllCall("gdiplus\GdipCreatePen1", "UInt", ARGB, "float", w, "int", 2, A_PtrSize ? "UPtr*" : "UInt*", pPen)
   return pPen
}

;-------------------------------------------------------------------------------------

Gdip_CreatePenFromBrush(pBrush, w)
{
	DllCall("gdiplus\GdipCreatePen2", A_PtrSize ? "UPtr" : "UInt", pBrush, "float", w, "int", 2, A_PtrSize ? "UPtr*" : "UInt*", pPen)
	return pPen
}

;-------------------------------------------------------------------------------------

Gdip_BrushCreateSolid(ARGB=0xff000000)
{
	DllCall("gdiplus\GdipCreateSolidFill", "UInt", ARGB, A_PtrSize ? "UPtr*" : "UInt*", pBrush)
	return pBrush
}

;-------------------------------------------------------------------------------------

; HatchStyleHorizontal = 0
; HatchStyleVertical = 1
; HatchStyleForwardDiagonal = 2
; HatchStyleBackwardDiagonal = 3
; HatchStyleCross = 4
; HatchStyleDiagonalCross = 5
; HatchStyle05Percent = 6
; HatchStyle10Percent = 7
; HatchStyle20Percent = 8
; HatchStyle25Percent = 9
; HatchStyle30Percent = 10
; HatchStyle40Percent = 11
; HatchStyle50Percent = 12
; HatchStyle60Percent = 13
; HatchStyle70Percent = 14
; HatchStyle75Percent = 15
; HatchStyle80Percent = 16
; HatchStyle90Percent = 17
; HatchStyleLightDownwardDiagonal = 18
; HatchStyleLightUpwardDiagonal = 19
; HatchStyleDarkDownwardDiagonal = 20
; HatchStyleDarkUpwardDiagonal = 21
; HatchStyleWideDownwardDiagonal = 22
; HatchStyleWideUpwardDiagonal = 23
; HatchStyleLightVertical = 24
; HatchStyleLightHorizontal = 25
; HatchStyleNarrowVertical = 26
; HatchStyleNarrowHorizontal = 27
; HatchStyleDarkVertical = 28
; HatchStyleDarkHorizontal = 29
; HatchStyleDashedDownwardDiagonal = 30
; HatchStyleDashedUpwardDiagonal = 31
; HatchStyleDashedHorizontal = 32
; HatchStyleDashedVertical = 33
; HatchStyleSmallConfetti = 34
; HatchStyleLargeConfetti = 35
; HatchStyleZigZag = 36
; HatchStyleWave = 37
; HatchStyleDiagonalBrick = 38
; HatchStyleHorizontalBrick = 39
; HatchStyleWeave = 40
; HatchStylePlaid = 41
; HatchStyleDivot = 42
; HatchStyleDottedGrid = 43
; HatchStyleDottedDiamond = 44
; HatchStyleShingle = 45
; HatchStyleTrellis = 46
; HatchStyleSphere = 47
; HatchStyleSmallGrid = 48
; HatchStyleSmallCheckerBoard = 49
; HatchStyleLargeCheckerBoard = 50
; HatchStyleOutlinedDiamond = 51
; HatchStyleSolidDiamond = 52
; HatchStyleTotal = 53
Gdip_BrushCreateHatch(ARGBfront, ARGBback, HatchStyle=0)
{
	DllCall("gdiplus\GdipCreateHatchBrush", "int", HatchStyle, "UInt", ARGBfront, "UInt", ARGBback, A_PtrSize ? "UPtr*" : "UInt*", pBrush)
	return pBrush
}

;-------------------------------------------------------------------------------------

Gdip_CreateTextureBrush(pBitmap, WrapMode=1, x=0, y=0, w="", h="")
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	, PtrA := A_PtrSize ? "UPtr*" : "UInt*"
	
	if !(w && h)
		DllCall("gdiplus\GdipCreateTexture", Ptr, pBitmap, "int", WrapMode, PtrA, pBrush)
	else
		DllCall("gdiplus\GdipCreateTexture2", Ptr, pBitmap, "int", WrapMode, "float", x, "float", y, "float", w, "float", h, PtrA, pBrush)
	return pBrush
}

;-------------------------------------------------------------------------------------

; WrapModeTile = 0
; WrapModeTileFlipX = 1
; WrapModeTileFlipY = 2
; WrapModeTileFlipXY = 3
; WrapModeClamp = 4
Gdip_CreateLineBrush(x1, y1, x2, y2, ARGB1, ARGB2, WrapMode=1)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	CreatePointF(PointF1, x1, y1), CreatePointF(PointF2, x2, y2)
	DllCall("gdiplus\GdipCreateLineBrush", Ptr, &PointF1, Ptr, &PointF2, "Uint", ARGB1, "Uint", ARGB2, "int", WrapMode, A_PtrSize ? "UPtr*" : "UInt*", LGpBrush)
	return LGpBrush
}

;-------------------------------------------------------------------------------------

; LinearGradientModeHorizontal = 0
; LinearGradientModeVertical = 1
; LinearGradientModeForwardDiagonal = 2
; LinearGradientModeBackwardDiagonal = 3
Gdip_CreateLineBrushFromRect(x, y, w, h, ARGB1, ARGB2, LinearGradientMode=1, WrapMode=1)
{
	CreateRectF(RectF, x, y, w, h)
	DllCall("gdiplus\GdipCreateLineBrushFromRect", A_PtrSize ? "UPtr" : "UInt", &RectF, "int", ARGB1, "int", ARGB2, "int", LinearGradientMode, "int", WrapMode, A_PtrSize ? "UPtr*" : "UInt*", LGpBrush)
	return LGpBrush
}

;-------------------------------------------------------------------------------------

Gdip_CloneBrush(pBrush)
{
	DllCall("gdiplus\GdipCloneBrush", A_PtrSize ? "UPtr" : "UInt", pBrush, A_PtrSize ? "UPtr*" : "UInt*", pBrushClone)
	return pBrushClone
}

;-------------------------------------------------------------------------------------
; Delete resources
;-------------------------------------------------------------------------------------

Gdip_DeletePen(pPen)
{
   return DllCall("gdiplus\GdipDeletePen", A_PtrSize ? "UPtr" : "UInt", pPen)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteBrush(pBrush)
{
   return DllCall("gdiplus\GdipDeleteBrush", A_PtrSize ? "UPtr" : "UInt", pBrush)
}

;-------------------------------------------------------------------------------------

Gdip_DisposeImage(pBitmap)
{
   return DllCall("gdiplus\GdipDisposeImage", A_PtrSize ? "UPtr" : "UInt", pBitmap)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteGraphics(pGraphics)
{
   return DllCall("gdiplus\GdipDeleteGraphics", A_PtrSize ? "UPtr" : "UInt", pGraphics)
}

;-------------------------------------------------------------------------------------

Gdip_DisposeImageAttributes(ImageAttr)
{
	return DllCall("gdiplus\GdipDisposeImageAttributes", A_PtrSize ? "UPtr" : "UInt", ImageAttr)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteFont(hFont)
{
   return DllCall("gdiplus\GdipDeleteFont", A_PtrSize ? "UPtr" : "UInt", hFont)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteStringFormat(hFormat)
{
   return DllCall("gdiplus\GdipDeleteStringFormat", A_PtrSize ? "UPtr" : "UInt", hFormat)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteFontFamily(hFamily)
{
   return DllCall("gdiplus\GdipDeleteFontFamily", A_PtrSize ? "UPtr" : "UInt", hFamily)
}

;-------------------------------------------------------------------------------------

Gdip_DeleteMatrix(Matrix)
{
   return DllCall("gdiplus\GdipDeleteMatrix", A_PtrSize ? "UPtr" : "UInt", Matrix)
}

;-------------------------------------------------------------------------------------
; Text functions
;-------------------------------------------------------------------------------------

Gdip_TextToGraphics(pGraphics, Text, Options, Font="Arial", Width="", Height="", Measure=0)
{
	IWidth := Width, IHeight:= Height
	
	RegExMatch(Options, "i)X([\-\d\.]+)(p*)", xpos)
	RegExMatch(Options, "i)Y([\-\d\.]+)(p*)", ypos)
	RegExMatch(Options, "i)W([\-\d\.]+)(p*)", Width)
	RegExMatch(Options, "i)H([\-\d\.]+)(p*)", Height)
	RegExMatch(Options, "i)C(?!(entre|enter))([a-f\d]+)", Colour)
	RegExMatch(Options, "i)Top|Up|Bottom|Down|vCentre|vCenter", vPos)
	RegExMatch(Options, "i)NoWrap", NoWrap)
	RegExMatch(Options, "i)R(\d)", Rendering)
	RegExMatch(Options, "i)S(\d+)(p*)", Size)

	if !Gdip_DeleteBrush(Gdip_CloneBrush(Colour2))
		PassBrush := 1, pBrush := Colour2
	
	if !(IWidth && IHeight) && (xpos2 || ypos2 || Width2 || Height2 || Size2)
		return -1

	Style := 0, Styles := "Regular|Bold|Italic|BoldItalic|Underline|Strikeout"
	Loop, Parse, Styles, |
	{
		if RegExMatch(Options, "\b" A_loopField)
		Style |= (A_LoopField != "StrikeOut") ? (A_Index-1) : 8
	}
  
	Align := 0, Alignments := "Near|Left|Centre|Center|Far|Right"
	Loop, Parse, Alignments, |
	{
		if RegExMatch(Options, "\b" A_loopField)
			Align |= A_Index//2.1      ; 0|0|1|1|2|2
	}

	xpos := (xpos1 != "") ? xpos2 ? IWidth*(xpos1/100) : xpos1 : 0
	ypos := (ypos1 != "") ? ypos2 ? IHeight*(ypos1/100) : ypos1 : 0
	Width := Width1 ? Width2 ? IWidth*(Width1/100) : Width1 : IWidth
	Height := Height1 ? Height2 ? IHeight*(Height1/100) : Height1 : IHeight
	if !PassBrush
		Colour := "0x" (Colour2 ? Colour2 : "ff000000")
	Rendering := ((Rendering1 >= 0) && (Rendering1 <= 5)) ? Rendering1 : 4
	Size := (Size1 > 0) ? Size2 ? IHeight*(Size1/100) : Size1 : 12

	hFamily := Gdip_FontFamilyCreate(Font)
	hFont := Gdip_FontCreate(hFamily, Size, Style)
	FormatStyle := NoWrap ? 0x4000 | 0x1000 : 0x4000
	hFormat := Gdip_StringFormatCreate(FormatStyle)
	pBrush := PassBrush ? pBrush : Gdip_BrushCreateSolid(Colour)
	if !(hFamily && hFont && hFormat && pBrush && pGraphics)
		return !pGraphics ? -2 : !hFamily ? -3 : !hFont ? -4 : !hFormat ? -5 : !pBrush ? -6 : 0
   
	CreateRectF(RC, xpos, ypos, Width, Height)
	Gdip_SetStringFormatAlign(hFormat, Align)
	Gdip_SetTextRenderingHint(pGraphics, Rendering)
	ReturnRC := Gdip_MeasureString(pGraphics, Text, hFont, hFormat, RC)

	if vPos
	{
		StringSplit, ReturnRC, ReturnRC, |
		
		if (vPos = "vCentre") || (vPos = "vCenter")
			ypos += (Height-ReturnRC4)//2
		else if (vPos = "Top") || (vPos = "Up")
			ypos := 0
		else if (vPos = "Bottom") || (vPos = "Down")
			ypos := Height-ReturnRC4
		
		CreateRectF(RC, xpos, ypos, Width, ReturnRC4)
		ReturnRC := Gdip_MeasureString(pGraphics, Text, hFont, hFormat, RC)
	}

	if !Measure
		E := Gdip_DrawString(pGraphics, Text, hFont, hFormat, pBrush, RC)

	if !PassBrush
		Gdip_DeleteBrush(pBrush)
	Gdip_DeleteStringFormat(hFormat)   
	Gdip_DeleteFont(hFont)
	Gdip_DeleteFontFamily(hFamily)
	return E ? E : ReturnRC
}

;-------------------------------------------------------------------------------------

Gdip_DrawString(pGraphics, sString, hFont, hFormat, pBrush, ByRef RectF)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if (!A_IsUnicode)
	{
		nSize := DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sString, "int", -1, Ptr, 0, "int", 0)
		VarSetCapacity(wString, nSize*2)
		DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sString, "int", -1, Ptr, &wString, "int", nSize)
	}
	
	return DllCall("gdiplus\GdipDrawString"
					, Ptr, pGraphics
					, Ptr, A_IsUnicode ? &sString : &wString
					, "int", -1
					, Ptr, hFont
					, Ptr, &RectF
					, Ptr, hFormat
					, Ptr, pBrush)
}

;-------------------------------------------------------------------------------------

Gdip_MeasureString(pGraphics, sString, hFont, hFormat, ByRef RectF)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	VarSetCapacity(RC, 16)
	if !A_IsUnicode
	{
		nSize := DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sString, "int", -1, "uint", 0, "int", 0)
		VarSetCapacity(wString, nSize*2)   
		DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sString, "int", -1, Ptr, &wString, "int", nSize)
	}
	
	DllCall("gdiplus\GdipMeasureString"
					, Ptr, pGraphics
					, Ptr, A_IsUnicode ? &sString : &wString
					, "int", -1
					, Ptr, hFont
					, Ptr, &RectF
					, Ptr, hFormat
					, Ptr, &RC
					, "uint*", Chars
					, "uint*", Lines)
	
	return &RC ? NumGet(RC, 0, "float") "|" NumGet(RC, 4, "float") "|" NumGet(RC, 8, "float") "|" NumGet(RC, 12, "float") "|" Chars "|" Lines : 0
}

; Near = 0
; Center = 1
; Far = 2
Gdip_SetStringFormatAlign(hFormat, Align)
{
   return DllCall("gdiplus\GdipSetStringFormatAlign", A_PtrSize ? "UPtr" : "UInt", hFormat, "int", Align)
}

; StringFormatFlagsDirectionRightToLeft    = 0x00000001
; StringFormatFlagsDirectionVertical       = 0x00000002
; StringFormatFlagsNoFitBlackBox           = 0x00000004
; StringFormatFlagsDisplayFormatControl    = 0x00000020
; StringFormatFlagsNoFontFallback          = 0x00000400
; StringFormatFlagsMeasureTrailingSpaces   = 0x00000800
; StringFormatFlagsNoWrap                  = 0x00001000
; StringFormatFlagsLineLimit               = 0x00002000
; StringFormatFlagsNoClip                  = 0x00004000 
Gdip_StringFormatCreate(Format=0, Lang=0)
{
   DllCall("gdiplus\GdipCreateStringFormat", "int", Format, "int", Lang, A_PtrSize ? "UPtr*" : "UInt*", hFormat)
   return hFormat
}

; Regular = 0
; Bold = 1
; Italic = 2
; BoldItalic = 3
; Underline = 4
; Strikeout = 8
Gdip_FontCreate(hFamily, Size, Style=0)
{
   DllCall("gdiplus\GdipCreateFont", A_PtrSize ? "UPtr" : "UInt", hFamily, "float", Size, "int", Style, "int", 0, A_PtrSize ? "UPtr*" : "UInt*", hFont)
   return hFont
}

Gdip_FontFamilyCreate(Font)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if (!A_IsUnicode)
	{
		nSize := DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &Font, "int", -1, "uint", 0, "int", 0)
		VarSetCapacity(wFont, nSize*2)
		DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &Font, "int", -1, Ptr, &wFont, "int", nSize)
	}
	
	DllCall("gdiplus\GdipCreateFontFamilyFromName"
					, Ptr, A_IsUnicode ? &Font : &wFont
					, "uint", 0
					, A_PtrSize ? "UPtr*" : "UInt*", hFamily)
	
	return hFamily
}

;-------------------------------------------------------------------------------------
; Matrix functions
;-------------------------------------------------------------------------------------

Gdip_CreateAffineMatrix(m11, m12, m21, m22, x, y)
{
   DllCall("gdiplus\GdipCreateMatrix2", "float", m11, "float", m12, "float", m21, "float", m22, "float", x, "float", y, A_PtrSize ? "UPtr*" : "UInt*", Matrix)
   return Matrix
}

Gdip_CreateMatrix()
{
   DllCall("gdiplus\GdipCreateMatrix", A_PtrSize ? "UPtr*" : "UInt*", Matrix)
   return Matrix
}

;-------------------------------------------------------------------------------------
; GraphicsPath functions
;-------------------------------------------------------------------------------------

; Alternate = 0
; Winding = 1
Gdip_CreatePath(BrushMode=0)
{
	DllCall("gdiplus\GdipCreatePath", "int", BrushMode, A_PtrSize ? "UPtr*" : "UInt*", Path)
	return Path
}

Gdip_AddPathEllipse(Path, x, y, w, h)
{
	return DllCall("gdiplus\GdipAddPathEllipse", A_PtrSize ? "UPtr" : "UInt", Path, "float", x, "float", y, "float", w, "float", h)
}

Gdip_AddPathPolygon(Path, Points)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	StringSplit, Points, Points, |
	VarSetCapacity(PointF, 8*Points0)   
	Loop, %Points0%
	{
		StringSplit, Coord, Points%A_Index%, `,
		NumPut(Coord1, PointF, 8*(A_Index-1), "float"), NumPut(Coord2, PointF, (8*(A_Index-1))+4, "float")
	}   

	return DllCall("gdiplus\GdipAddPathPolygon", Ptr, Path, Ptr, &PointF, "int", Points0)
}

Gdip_DeletePath(Path)
{
	return DllCall("gdiplus\GdipDeletePath", A_PtrSize ? "UPtr" : "UInt", Path)
}

;-------------------------------------------------------------------------------------
; Quality functions
;-------------------------------------------------------------------------------------

; SystemDefault = 0
; SingleBitPerPixelGridFit = 1
; SingleBitPerPixel = 2
; AntiAliasGridFit = 3
; AntiAlias = 4
Gdip_SetTextRenderingHint(pGraphics, RenderingHint)
{
	return DllCall("gdiplus\GdipSetTextRenderingHint", A_PtrSize ? "UPtr" : "UInt", pGraphics, "int", RenderingHint)
}

; Default = 0
; LowQuality = 1
; HighQuality = 2
; Bilinear = 3
; Bicubic = 4
; NearestNeighbor = 5
; HighQualityBilinear = 6
; HighQualityBicubic = 7
Gdip_SetInterpolationMode(pGraphics, InterpolationMode)
{
   return DllCall("gdiplus\GdipSetInterpolationMode", A_PtrSize ? "UPtr" : "UInt", pGraphics, "int", InterpolationMode)
}

; Default = 0
; HighSpeed = 1
; HighQuality = 2
; None = 3
; AntiAlias = 4
Gdip_SetSmoothingMode(pGraphics, SmoothingMode)
{
   return DllCall("gdiplus\GdipSetSmoothingMode", A_PtrSize ? "UPtr" : "UInt", pGraphics, "int", SmoothingMode)
}

; CompositingModeSourceOver = 0 (blended)
; CompositingModeSourceCopy = 1 (overwrite)
Gdip_SetCompositingMode(pGraphics, CompositingMode=0)
{
   return DllCall("gdiplus\GdipSetCompositingMode", A_PtrSize ? "UPtr" : "UInt", pGraphics, "int", CompositingMode)
}

;-------------------------------------------------------------------------------------
; Extra functions
;-------------------------------------------------------------------------------------

Gdip_Startup()
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if !DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
		DllCall("LoadLibrary", "str", "gdiplus")
	VarSetCapacity(si, A_PtrSize = 8 ? 24 : 16, 0), si := Chr(1)
	DllCall("gdiplus\GdiplusStartup", A_PtrSize ? "UPtr*" : "uint*", pToken, Ptr, &si, Ptr, 0)
	return pToken
}

Gdip_Shutdown(pToken)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	DllCall("gdiplus\GdiplusShutdown", Ptr, pToken)
	if hModule := DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
		DllCall("FreeLibrary", Ptr, hModule)
	return 0
}

; Prepend = 0; The new operation is applied before the old operation.
; Append = 1; The new operation is applied after the old operation.
Gdip_RotateWorldTransform(pGraphics, Angle, MatrixOrder=0)
{
	return DllCall("gdiplus\GdipRotateWorldTransform", A_PtrSize ? "UPtr" : "UInt", pGraphics, "float", Angle, "int", MatrixOrder)
}

Gdip_ScaleWorldTransform(pGraphics, x, y, MatrixOrder=0)
{
	return DllCall("gdiplus\GdipScaleWorldTransform", A_PtrSize ? "UPtr" : "UInt", pGraphics, "float", x, "float", y, "int", MatrixOrder)
}

Gdip_TranslateWorldTransform(pGraphics, x, y, MatrixOrder=0)
{
	return DllCall("gdiplus\GdipTranslateWorldTransform", A_PtrSize ? "UPtr" : "UInt", pGraphics, "float", x, "float", y, "int", MatrixOrder)
}

Gdip_ResetWorldTransform(pGraphics)
{
	return DllCall("gdiplus\GdipResetWorldTransform", A_PtrSize ? "UPtr" : "UInt", pGraphics)
}

Gdip_GetRotatedTranslation(Width, Height, Angle, ByRef xTranslation, ByRef yTranslation)
{
	pi := 3.14159, TAngle := Angle*(pi/180)	

	Bound := (Angle >= 0) ? Mod(Angle, 360) : 360-Mod(-Angle, -360)
	if ((Bound >= 0) && (Bound <= 90))
		xTranslation := Height*Sin(TAngle), yTranslation := 0
	else if ((Bound > 90) && (Bound <= 180))
		xTranslation := (Height*Sin(TAngle))-(Width*Cos(TAngle)), yTranslation := -Height*Cos(TAngle)
	else if ((Bound > 180) && (Bound <= 270))
		xTranslation := -(Width*Cos(TAngle)), yTranslation := -(Height*Cos(TAngle))-(Width*Sin(TAngle))
	else if ((Bound > 270) && (Bound <= 360))
		xTranslation := 0, yTranslation := -Width*Sin(TAngle)
}

Gdip_GetRotatedDimensions(Width, Height, Angle, ByRef RWidth, ByRef RHeight)
{
	pi := 3.14159, TAngle := Angle*(pi/180)
	if !(Width && Height)
		return -1
	RWidth := Ceil(Abs(Width*Cos(TAngle))+Abs(Height*Sin(TAngle)))
	RHeight := Ceil(Abs(Width*Sin(TAngle))+Abs(Height*Cos(Tangle)))
}

; RotateNoneFlipNone   = 0
; Rotate90FlipNone     = 1
; Rotate180FlipNone    = 2
; Rotate270FlipNone    = 3
; RotateNoneFlipX      = 4
; Rotate90FlipX        = 5
; Rotate180FlipX       = 6
; Rotate270FlipX       = 7
; RotateNoneFlipY      = Rotate180FlipX
; Rotate90FlipY        = Rotate270FlipX
; Rotate180FlipY       = RotateNoneFlipX
; Rotate270FlipY       = Rotate90FlipX
; RotateNoneFlipXY     = Rotate180FlipNone
; Rotate90FlipXY       = Rotate270FlipNone
; Rotate180FlipXY      = RotateNoneFlipNone
; Rotate270FlipXY      = Rotate90FlipNone 

Gdip_ImageRotateFlip(pBitmap, RotateFlipType=1)
{
	return DllCall("gdiplus\GdipImageRotateFlip", A_PtrSize ? "UPtr" : "UInt", pBitmap, "int", RotateFlipType)
}

; Replace = 0
; Intersect = 1
; Union = 2
; Xor = 3
; Exclude = 4
; Complement = 5
Gdip_SetClipRect(pGraphics, x, y, w, h, CombineMode=0)
{
   return DllCall("gdiplus\GdipSetClipRect",  A_PtrSize ? "UPtr" : "UInt", pGraphics, "float", x, "float", y, "float", w, "float", h, "int", CombineMode)
}

Gdip_SetClipPath(pGraphics, Path, CombineMode=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	return DllCall("gdiplus\GdipSetClipPath", Ptr, pGraphics, Ptr, Path, "int", CombineMode)
}

Gdip_ResetClip(pGraphics)
{
   return DllCall("gdiplus\GdipResetClip", A_PtrSize ? "UPtr" : "UInt", pGraphics)
}

Gdip_GetClipRegion(pGraphics)
{
	Region := Gdip_CreateRegion()
	DllCall("gdiplus\GdipGetClip", A_PtrSize ? "UPtr" : "UInt", pGraphics, "UInt*", Region)
	return Region
}

Gdip_SetClipRegion(pGraphics, Region, CombineMode=0)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("gdiplus\GdipSetClipRegion", Ptr, pGraphics, Ptr, Region, "int", CombineMode)
}

Gdip_CreateRegion()
{
	DllCall("gdiplus\GdipCreateRegion", "UInt*", Region)
	return Region
}

Gdip_DeleteRegion(Region)
{
	return DllCall("gdiplus\GdipDeleteRegion", A_PtrSize ? "UPtr" : "UInt", Region)
}

;-------------------------------------------------------------------------------------
; BitmapLockBits
;-------------------------------------------------------------------------------------

Gdip_LockBits(pBitmap, x, y, w, h, ByRef Stride, ByRef Scan0, ByRef BitmapData, LockMode = 3, PixelFormat = 0x26200a)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	CreateRect(Rect, x, y, w, h)
	VarSetCapacity(BitmapData, 16+2*(A_PtrSize ? A_PtrSize : 4), 0)
	E := DllCall("Gdiplus\GdipBitmapLockBits", Ptr, pBitmap, Ptr, &Rect, "uint", LockMode, "int", PixelFormat, Ptr, &BitmapData)
	Stride := NumGet(BitmapData, 8, "Int")
	Scan0 := NumGet(BitmapData, 16, Ptr)
	return E
}

;-------------------------------------------------------------------------------------

Gdip_UnlockBits(pBitmap, ByRef BitmapData)
{
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	return DllCall("Gdiplus\GdipBitmapUnlockBits", Ptr, pBitmap, Ptr, &BitmapData)
}

;-------------------------------------------------------------------------------------

Gdip_SetLockBitPixel(ARGB, Scan0, x, y, Stride)
{
	Numput(ARGB, Scan0+0, (x*4)+(y*Stride), "UInt")
}

;-------------------------------------------------------------------------------------

Gdip_GetLockBitPixel(Scan0, x, y, Stride)
{
	return NumGet(Scan0+0, (x*4)+(y*Stride), "UInt")
}

;-------------------------------------------------------------------------------------

Gdip_PixelateBitmap(pBitmap, ByRef pBitmapOut, BlockSize)
{
	static PixelateBitmap
	
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	
	if (!PixelateBitmap)
	{
		if A_PtrSize != 8 ; x86 machine code
		MCode_PixelateBitmap =
		(LTrim Join
		558BEC83EC3C8B4514538B5D1C99F7FB56578BC88955EC894DD885C90F8E830200008B451099F7FB8365DC008365E000894DC88955F08945E833FF897DD4
		397DE80F8E160100008BCB0FAFCB894DCC33C08945F88945FC89451C8945143BD87E608B45088D50028BC82BCA8BF02BF2418945F48B45E02955F4894DC4
		8D0CB80FAFCB03CA895DD08BD1895DE40FB64416030145140FB60201451C8B45C40FB604100145FC8B45F40FB604020145F883C204FF4DE475D6034D18FF
		4DD075C98B4DCC8B451499F7F98945148B451C99F7F989451C8B45FC99F7F98945FC8B45F899F7F98945F885DB7E648B450C8D50028BC82BCA83C103894D
		C48BC82BCA41894DF48B4DD48945E48B45E02955E48D0C880FAFCB03CA895DD08BD18BF38A45148B7DC48804178A451C8B7DF488028A45FC8804178A45F8
		8B7DE488043A83C2044E75DA034D18FF4DD075CE8B4DCC8B7DD447897DD43B7DE80F8CF2FEFFFF837DF0000F842C01000033C08945F88945FC89451C8945
		148945E43BD87E65837DF0007E578B4DDC034DE48B75E80FAF4D180FAFF38B45088D500203CA8D0CB18BF08BF88945F48B45F02BF22BFA2955F48945CC0F
		B6440E030145140FB60101451C0FB6440F010145FC8B45F40FB604010145F883C104FF4DCC75D8FF45E4395DE47C9B8B4DF00FAFCB85C9740B8B451499F7
		F9894514EB048365140033F63BCE740B8B451C99F7F989451CEB0389751C3BCE740B8B45FC99F7F98945FCEB038975FC3BCE740B8B45F899F7F98945F8EB
		038975F88975E43BDE7E5A837DF0007E4C8B4DDC034DE48B75E80FAF4D180FAFF38B450C8D500203CA8D0CB18BF08BF82BF22BFA2BC28B55F08955CC8A55
		1488540E038A551C88118A55FC88540F018A55F888140183C104FF4DCC75DFFF45E4395DE47CA68B45180145E0015DDCFF4DC80F8594FDFFFF8B451099F7
		FB8955F08945E885C00F8E450100008B45EC0FAFC38365DC008945D48B45E88945CC33C08945F88945FC89451C8945148945103945EC7E6085DB7E518B4D
		D88B45080FAFCB034D108D50020FAF4D18034DDC8BF08BF88945F403CA2BF22BFA2955F4895DC80FB6440E030145140FB60101451C0FB6440F010145FC8B
		45F40FB604080145F883C104FF4DC875D8FF45108B45103B45EC7CA08B4DD485C9740B8B451499F7F9894514EB048365140033F63BCE740B8B451C99F7F9
		89451CEB0389751C3BCE740B8B45FC99F7F98945FCEB038975FC3BCE740B8B45F899F7F98945F8EB038975F88975103975EC7E5585DB7E468B4DD88B450C
		0FAFCB034D108D50020FAF4D18034DDC8BF08BF803CA2BF22BFA2BC2895DC88A551488540E038A551C88118A55FC88540F018A55F888140183C104FF4DC8
		75DFFF45108B45103B45EC7CAB8BC3C1E0020145DCFF4DCC0F85CEFEFFFF8B4DEC33C08945F88945FC89451C8945148945103BC87E6C3945F07E5C8B4DD8
		8B75E80FAFCB034D100FAFF30FAF4D188B45088D500203CA8D0CB18BF08BF88945F48B45F02BF22BFA2955F48945C80FB6440E030145140FB60101451C0F
		B6440F010145FC8B45F40FB604010145F883C104FF4DC875D833C0FF45108B4DEC394D107C940FAF4DF03BC874068B451499F7F933F68945143BCE740B8B
		451C99F7F989451CEB0389751C3BCE740B8B45FC99F7F98945FCEB038975FC3BCE740B8B45F899F7F98945F8EB038975F88975083975EC7E63EB0233F639
		75F07E4F8B4DD88B75E80FAFCB034D080FAFF30FAF4D188B450C8D500203CA8D0CB18BF08BF82BF22BFA2BC28B55F08955108A551488540E038A551C8811
		8A55FC88540F018A55F888140883C104FF4D1075DFFF45088B45083B45EC7C9F5F5E33C05BC9C21800
		)
		else ; x64 machine code
		MCode_PixelateBitmap =
		(LTrim Join
		4489442418488954241048894C24085355565741544155415641574883EC28418BC1448B8C24980000004C8BDA99488BD941F7F9448BD0448BFA8954240C
		448994248800000085C00F8E9D020000418BC04533E4458BF299448924244C8954241041F7F933C9898C24980000008BEA89542404448BE889442408EB05
		4C8B5C24784585ED0F8E1A010000458BF1418BFD48897C2418450FAFF14533D233F633ED4533E44533ED4585C97E5B4C63BC2490000000418D040A410FAF
		C148984C8D441802498BD9498BD04D8BD90FB642010FB64AFF4403E80FB60203E90FB64AFE4883C2044403E003F149FFCB75DE4D03C748FFCB75D0488B7C
		24188B8C24980000004C8B5C2478418BC59941F7FE448BE8418BC49941F7FE448BE08BC59941F7FE8BE88BC69941F7FE8BF04585C97E4048639C24900000
		004103CA4D8BC1410FAFC94863C94A8D541902488BCA498BC144886901448821408869FF408871FE4883C10448FFC875E84803D349FFC875DA8B8C249800
		0000488B5C24704C8B5C24784183C20448FFCF48897C24180F850AFFFFFF8B6C2404448B2424448B6C24084C8B74241085ED0F840A01000033FF33DB4533
		DB4533D24533C04585C97E53488B74247085ED7E42438D0C04418BC50FAF8C2490000000410FAFC18D04814863C8488D5431028BCD0FB642014403D00FB6
		024883C2044403D80FB642FB03D80FB642FA03F848FFC975DE41FFC0453BC17CB28BCD410FAFC985C9740A418BC299F7F98BF0EB0233F685C9740B418BC3
		99F7F9448BD8EB034533DB85C9740A8BC399F7F9448BD0EB034533D285C9740A8BC799F7F9448BC0EB034533C033D24585C97E4D4C8B74247885ED7E3841
		8D0C14418BC50FAF8C2490000000410FAFC18D04814863C84A8D4431028BCD40887001448818448850FF448840FE4883C00448FFC975E8FFC2413BD17CBD
		4C8B7424108B8C2498000000038C2490000000488B5C24704503E149FFCE44892424898C24980000004C897424100F859EFDFFFF448B7C240C448B842480
		000000418BC09941F7F98BE8448BEA89942498000000896C240C85C00F8E3B010000448BAC2488000000418BCF448BF5410FAFC9898C248000000033FF33
		ED33F64533DB4533D24533C04585FF7E524585C97E40418BC5410FAFC14103C00FAF84249000000003C74898488D541802498BD90FB642014403D00FB602
		4883C2044403D80FB642FB03F00FB642FA03E848FFCB75DE488B5C247041FFC0453BC77CAE85C9740B418BC299F7F9448BE0EB034533E485C9740A418BC3
		99F7F98BD8EB0233DB85C9740A8BC699F7F9448BD8EB034533DB85C9740A8BC599F7F9448BD0EB034533D24533C04585FF7E4E488B4C24784585C97E3541
		8BC5410FAFC14103C00FAF84249000000003C74898488D540802498BC144886201881A44885AFF448852FE4883C20448FFC875E941FFC0453BC77CBE8B8C
		2480000000488B5C2470418BC1C1E00203F849FFCE0F85ECFEFFFF448BAC24980000008B6C240C448BA4248800000033FF33DB4533DB4533D24533C04585
		FF7E5A488B7424704585ED7E48418BCC8BC5410FAFC94103C80FAF8C2490000000410FAFC18D04814863C8488D543102418BCD0FB642014403D00FB60248
		83C2044403D80FB642FB03D80FB642FA03F848FFC975DE41FFC0453BC77CAB418BCF410FAFCD85C9740A418BC299F7F98BF0EB0233F685C9740B418BC399
		F7F9448BD8EB034533DB85C9740A8BC399F7F9448BD0EB034533D285C9740A8BC799F7F9448BC0EB034533C033D24585FF7E4E4585ED7E42418BCC8BC541
		0FAFC903CA0FAF8C2490000000410FAFC18D04814863C8488B442478488D440102418BCD40887001448818448850FF448840FE4883C00448FFC975E8FFC2
		413BD77CB233C04883C428415F415E415D415C5F5E5D5BC3
		)
		
		VarSetCapacity(PixelateBitmap, StrLen(MCode_PixelateBitmap)//2)
		Loop % StrLen(MCode_PixelateBitmap)//2		;%
			NumPut("0x" SubStr(MCode_PixelateBitmap, (2*A_Index)-1, 2), PixelateBitmap, A_Index-1, "UChar")
		DllCall("VirtualProtect", Ptr, &PixelateBitmap, Ptr, VarSetCapacity(PixelateBitmap), "uint", 0x40, A_PtrSize ? "UPtr*" : "UInt*", 0)
	}

	Gdip_GetImageDimensions(pBitmap, Width, Height)
	
	if (Width != Gdip_GetImageWidth(pBitmapOut) || Height != Gdip_GetImageHeight(pBitmapOut))
		return -1
	if (BlockSize > Width || BlockSize > Height)
		return -2

	E1 := Gdip_LockBits(pBitmap, 0, 0, Width, Height, Stride1, Scan01, BitmapData1)
	E2 := Gdip_LockBits(pBitmapOut, 0, 0, Width, Height, Stride2, Scan02, BitmapData2)
	if (E1 || E2)
		return -3

	E := DllCall(&PixelateBitmap, Ptr, Scan01, Ptr, Scan02, "int", Width, "int", Height, "int", Stride1, "int", BlockSize)
	
	Gdip_UnlockBits(pBitmap, BitmapData1), Gdip_UnlockBits(pBitmapOut, BitmapData2)
	return 0
}

;-------------------------------------------------------------------------------------

Gdip_ToARGB(A, R, G, B)
{
	return (A << 24) | (R << 16) | (G << 8) | B
}

;-------------------------------------------------------------------------------------

Gdip_FromARGB(ARGB, ByRef A, ByRef R, ByRef G, ByRef B)
{
	A := (0xff000000 & ARGB) >> 24
	R := (0x00ff0000 & ARGB) >> 16
	G := (0x0000ff00 & ARGB) >> 8
	B := 0x000000ff & ARGB
}

;-------------------------------------------------------------------------------------

Gdip_AFromARGB(ARGB)
{
	return (0xff000000 & ARGB) >> 24
}

;-------------------------------------------------------------------------------------

Gdip_RFromARGB(ARGB)
{
	return (0x00ff0000 & ARGB) >> 16
}

;-------------------------------------------------------------------------------------

Gdip_GFromARGB(ARGB)
{
	return (0x0000ff00 & ARGB) >> 8
}

;-------------------------------------------------------------------------------------

Gdip_BFromARGB(ARGB)
{
	return 0x000000ff & ARGB
}

;-------------------------------------------------------------------------------------

StrGetB(Address, Length=-1, Encoding=0)
{
	; Flexible parameter handling:
	if Length is not integer
	Encoding := Length,  Length := -1

	; Check for obvious errors.
	if (Address+0 < 1024)
		return

	; Ensure 'Encoding' contains a numeric identifier.
	if Encoding = UTF-16
		Encoding = 1200
	else if Encoding = UTF-8
		Encoding = 65001
	else if SubStr(Encoding,1,2)="CP"
		Encoding := SubStr(Encoding,3)

	if !Encoding ; "" or 0
	{
		; No conversion necessary, but we might not want the whole string.
		if (Length == -1)
			Length := DllCall("lstrlen", "uint", Address)
		VarSetCapacity(String, Length)
		DllCall("lstrcpyn", "str", String, "uint", Address, "int", Length + 1)
	}
	else if Encoding = 1200 ; UTF-16
	{
		char_count := DllCall("WideCharToMultiByte", "uint", 0, "uint", 0x400, "uint", Address, "int", Length, "uint", 0, "uint", 0, "uint", 0, "uint", 0)
		VarSetCapacity(String, char_count)
		DllCall("WideCharToMultiByte", "uint", 0, "uint", 0x400, "uint", Address, "int", Length, "str", String, "int", char_count, "uint", 0, "uint", 0)
	}
	else if Encoding is integer
	{
		; Convert from target encoding to UTF-16 then to the active code page.
		char_count := DllCall("MultiByteToWideChar", "uint", Encoding, "uint", 0, "uint", Address, "int", Length, "uint", 0, "int", 0)
		VarSetCapacity(String, char_count * 2)
		char_count := DllCall("MultiByteToWideChar", "uint", Encoding, "uint", 0, "uint", Address, "int", Length, "uint", &String, "int", char_count * 2)
		String := StrGetB(&String, char_count, 1200)
	}
	
	return String
}
Screenshot(outfile)
{
    pToken := Gdip_Startup()
    ;獲取顯示器總數
    SysGet, __nb_monitor, MonitorCount
    _A_ScreenWidth:=A_ScreenWidth*__nb_monitor
    screen=0|0|%_A_ScreenWidth%|%A_ScreenHeight%
    pBitmap := Gdip_BitmapFromScreen(screen)

    Gdip_SaveBitmapToFile(pBitmap, outfile, 100)
    Gdip_DisposeImage(pBitmap)
    Gdip_Shutdown(pToken)
}
'''},
    #endregion Screenshot
}
#endregion 腳本函數字典


#定義函式:將xml格式化
def FormatXML(xml_str):
    xml_str=FormatHTML(xml_str)
    xml_str_line_list=xml_str.split('\n')
    xml_str_line_list=[xml_str_line for xml_str_line in xml_str_line_list if xml_str_line.strip()!=""]
    return "\n".join(xml_str_line_list)

#定義動作:尋找該層下的選擇器
def FindCurrent(elt,css_selector,get_one=True):
    if not elt:
        return None
    com_elt_list=[elt_child for elt_child in elt.select(css_selector) if elt_child.parent==elt]
    if get_one:
        if com_elt_list:
            return com_elt_list[0]
        else:
            return None
    else:
        return com_elt_list

#設置解析xml用的隱藏div容器
div_xml_elt=DIV(id="div_xml",style={'display':'none'})
doc<=div_xml_elt

#定義動作:轉換xml為block
def XmlToBlockly(ev):
    #若xml的更改事件不是起源於blockly，就繼續執行
    if not hasattr(ev,"changeStartFromBlockly"):
        #print('xml>block')
        #獲取textarea_xml元素中的xml_str
        textarea_elt=doc['textarea_xml']
        xml_str=textarea_elt.value
        #製作臨時div容器以生成xml元素
        div_xml_elt=doc["div_xml"]
        div_xml_elt.innerHTML=xml_str
        xml_elt=div_xml_elt.select_one('xml')
        #若xml元素產生成功，就將xml元素嵌入至blockly區塊顯示
        if xml_elt:
            Blockly.Xml.clearWorkspaceAndLoadFromXml(xml_elt,workspace)
        #輸出格式化xml到
        xml_format_str=FormatXML(textarea_elt.value)
        textarea_elt.value=xml_format_str
        
#定義動作:顯示blocks的xml (必須等待Block載入完成)
def BlocklyToXml(ev):
    #啟用複製和下載AHK檔案按鈕
    for btn_elt in doc['div_copy_ahkfile_btns_area'].select('button'):
        btn_elt.disabled=False
        btn_elt.classList.remove('disabled_button')
    #print('block>xml')
    #自blockly獲取xml_str
    xml_blockly_elt=Blockly.Xml.workspaceToDom(workspace)
    doc['textarea_xml'].value=FormatXML(xml_blockly_elt.outerHTML)
    #製作input事件，觸發XmlToAHK，並附加起源資訊到事件元素中
    input_ev = window.Event.new("input")
    input_ev.changeStartFromBlockly=True
    doc['textarea_xml'].dispatchEvent(input_ev)


#預設欲生成後來要追加在AHK腳本置頂處或最尾處的字典鍵值集合
func_dict_key_set=set()
#定義動作:轉譯xml為AHK語法
def XmlToAHK(ev):
    #藉由點擊觸發轉譯事件
    if ev.type in ["input","click"]:
        global func_dict_key_set
        #清空:預設欲生成後來要追加在AHK腳本置頂處或最尾處的字典鍵值集合
        func_dict_key_set=set()

        ##註冊物件型Block元素列表 (不能被獨立轉譯)
        OBJ_BLOCK_LIST=[
            'function_key',
            'special_key',
            'normal_key',
            'filepath',
            'text',
            'webpage',
            'built_in_program',
            'built_in_dirpath',
            'built_in_webpage',
            'path_combined',
            'built_in_time',
            'math_arithmetic',
            'math_number',
            'variables_get',
            'logic_boolean',
            'logic_compare',
            'logic_operation',
            'logic_null',
            'logic_negate',
            'in_str',
            'right_click_menu', #不讓右鍵清單獨立執行，否則會無限循環跳出清單
            'get_key_state',
            'math_function',
            'math_function2',
            'math_constant2',
            'math_round',
            'math_mod',
            'lists_create_with',
            'list_str',
            'system_info_str',
            'system_info_num',
        ]
        #print('xml>ahk')
        # print('XmlToAHK',"ev.type:",ev.type)

        #至textarea_xml元素獲取xml
        textarea_xml_elt=ev.currentTarget
        xml_str=textarea_xml_elt.value
        #獲取要輸出到指定的textarea元素
        textarea_ahk_elt=doc['textarea_ahk']

        #預設生成AHK程式碼
        ahk_code=""
        
        #建立暫時的div容器用來解析xml
        div_parseXml_elt=DIV()
        div_parseXml_elt.innerHTML=xml_str
        block_elt_list=div_parseXml_elt.select('xml>block')

#endregion

        
        
        #將逐個blockly轉譯為AHK
        for block_elt in block_elt_list:
            #不要轉譯落單的field block
            if block_elt.attrs['type'] not in OBJ_BLOCK_LIST:
                ahk_code+=AHK_block(block_elt)+'\n'

    
        #預設欲生成後來要追加在AHK腳本置頂處或最尾處的字典鍵值集合
        pre_ahk_code=""
        end_ahk_code=""
        #根據關聯函數字典鍵值集合生成前置和後置程式碼
        for func_dict_key in func_dict_key_set:
            pre_ahk_code+=FUNC_DICT[func_dict_key].get('pre','')
            end_ahk_code+=FUNC_DICT[func_dict_key].get('end','')


        #為AHK碼加上前段程式碼
        ahk_code=";請確保下段程式碼在腳本最頂部\n"*(pre_ahk_code!="") + pre_ahk_code + ";=====================\n\n"*(pre_ahk_code!="") + ahk_code
        
        #為AHK碼加上後段程式碼
        ahk_code+="\n;=====================\n"*(end_ahk_code!="") + end_ahk_code

        textarea_ahk_elt.innerHTML=ahk_code

        #移除暫時的div容器
        del div_parseXml_elt


#region 基本函數

#定義函數: 將半形符號轉換成全形符號
def ToFullWidthString(text,excluded_str_list=None):
    if not excluded_str_list:
        excluded_str_list=[]
    full_width_string_dict={
        r'~':'～',
        r'!':'！',
        r'@':'＠',
        r'#':'＃',
        r'$':'＄',
        r'%':'％',
        r'^':'︿',
        r'&':'＆',
        r'*':'＊',
        r'(':'（',
        r')':'）',
        r'_':'＿',
        r'+':'＋',
        r'`':'‵',
        r'-':'－',
        r'=':'＝',
        r'{':'｛',
        r'}':'｝',
        r'[':'［',
        r']':'］',
        r':':'：',
        r';':'；',
        r'"':'＂',
        r"'":'’',
        r'<':'＜',
        r'>':'＞',
        r',':'，',
        r'.':'．',
        r'?':'？',
        r'/':'／',
        r'|':'｜',
        '\\':'＼',
        ' ':'_',
        "　":"_",
    }
    chr_set=set(text)
    com_text=str(text)
    #遍歷每一個字母
    for c in chr_set:
        #替換成全行字體 (排除提供的例外串列)
        if c in full_width_string_dict.keys() and c not in excluded_str_list:
            com_text=com_text.replace(c,full_width_string_dict[c])
    return com_text


#endregion 基本函數

#定義函式:抽出元素的註解
def Comment(elt,get_all_comment=False):
    com_str=""
    commit_elt_list=[]
    #判斷輸入的元素是否存在
    if elt:
        if get_all_comment:
            commit_elt_list=elt.select('comment')
        else:
            #搜尋該層下的comment
            commit_elt=FindCurrent(elt,'comment')
            #判斷該元素是否有comment
            if commit_elt:
                commit_elt_list.append(commit_elt)
        for commit_elt in commit_elt_list:
            commit_str=commit_elt.text
            #處理多行註解
            commit_str=commit_str.replace('\n','\n;')
            com_str+=f";{commit_str}\n"
            commit_elt.remove()
    
    return com_str

#定義函式:解析value元素為AHK語法
def AHK_value(value_elt,get_all_comment=False):
    if value_elt:
        block_underValue_elt=value_elt.select_one('block')
        return AHK_block(block_underValue_elt,get_all_comment=get_all_comment,separate_comment=True)
    else:
        return ("","")

#定義函式:解析statement元素為AHK語法
def AHK_statement(statement_elt,for_hotkey=False,Indentation=True):
    com_str=""
    if statement_elt:
        block_underStatement_elt=FindCurrent(statement_elt,'block')
        if block_underStatement_elt:
            statement_str=AHK_block(block_underStatement_elt)
            if for_hotkey:
                if statement_str.count('\n')>1 :
                    com_str+=f'\n{statement_str}Return\n'
                else:
                    com_str+=f"{statement_str}"
            else:
                #處理執行式縮排
                statement_str=TAB_SPACE*Indentation+statement_str.replace("\n","\n"+TAB_SPACE*Indentation)
                #去除執行式中空白的文字行
                statement_str='\n'.join([statement_str for statement_str in statement_str.split('\n') if statement_str.replace(';','').strip()!=""])+'\n'
                com_str+=statement_str
    return com_str


#定義函式:解析block元素為AHK語法
def AHK_block(block_elt,get_all_comment=False,separate_comment=False):
    #獲取全域變數:關聯函數字典鍵值集合
    global func_dict_key_set 

    # print(block_elt.attrs['type'])

    #預設輸出程式碼
    com_str=""
    #預設輸出註解
    comment_str=""

    #判斷是否要無視該Block
    block_is_disabled_bool=True
    if block_elt:
        #若該blockly已經被禁用，就不該轉譯這個Block
        if block_elt.attrs.get("disabled",None):
            if block_elt.attrs["disabled"]=="true":
                block_is_disabled_bool=True
            else:
                block_is_disabled_bool=False
        else:
            block_is_disabled_bool=False
    
    

    #若需要轉譯
    if not block_is_disabled_bool:
        comment_str+=Comment(block_elt,get_all_comment=get_all_comment)

        #region 按鍵Blockly

        if block_elt.attrs['type']=="hotkey_execute" or block_elt.attrs['type']=="hotkey_execute_with_setting":
            #預設輸出的ahk熱鍵碼
            hotkey_str=""
            #預設輸出的ahk執行碼
            statement_str=""
            #預設是否已#if結尾
            ending_with_if_bool=False

            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            if value_elt:
                #獲取功能鍵
                block_functionKey_elt_list=value_elt.select('block[type="function_key"]')
                for block_functionKey_elt in block_functionKey_elt_list:
                    functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                    hotkey_str+=functionKey_str
                    com_str+=functionKey_comment
                #獲取一般鍵
                block_normalKey_elt_list=value_elt.select('block[type="normal_key"]')
                block_normalKey_elt_list.extend(value_elt.select('block[type="special_key"]'))
                for block_normalKey_elt in block_normalKey_elt_list:
                    normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                    hotkey_str+=normalKey_str
                    com_str+=normalKey_comment
                #獲取執行元素
                statement_elt=FindCurrent(block_elt,'statement[name="DO"]')
                if statement_elt:
                    statement_str=AHK_statement(statement_elt,for_hotkey=True)

            #若為進階的熱鍵設定
            if block_elt.attrs['type']=="hotkey_execute_with_setting":
                #獲取熱鍵設定元素
                statement_elt=FindCurrent(block_elt,'statement[name="SETTING"]')
                if statement_elt:
                    #獲取所有設定註解
                    hotkey_setting_all_comment_str=Comment(statement_elt,get_all_comment=True)
                    com_str+=hotkey_setting_all_comment_str
                    #若設定避免自我觸發
                    if statement_elt.select_one('block[type="hotkey_execute_setting_donottriggeritself"]'):
                        hotkey_str='$'+hotkey_str
                    #若設定可被其他按鍵觸發
                    if statement_elt.select_one('block[type="hotkey_execute_setting_cantriggeronotherhotkey"]'):
                        hotkey_str='*'+hotkey_str
                    #若設定保持原有熱鍵功能
                    if statement_elt.select_one('block[type="hotkey_execute_setting_keepkeyfuncdefalut"]'):
                        hotkey_str='~'+hotkey_str
                    if statement_elt.select_one('block[type="hotkey_execute_setting_ifwinactive"]'):
                        #獲取標題文字元素
                        func_dict_key_set.update(['SetTitleMatchMode'])
                        block_ifwinactive_elt=statement_elt.select_one('block[type="hotkey_execute_setting_ifwinactive"]')
                        field_text_elt=FindCurrent(block_ifwinactive_elt,'field[name="text"]')
                        hotkey_str=f'#IfWinActive, {field_text_elt.text}\n'+hotkey_str
                        ending_with_if_bool=True

            com_str+=hotkey_str+f"::{statement_str}"+"#If"*ending_with_if_bool+"\n"
                
        elif block_elt.attrs['type']=="function_key":
            field_elt=FindCurrent(block_elt,'field')
            function_key_name=field_elt.text
            function_key_dict={
                'Ctrl':'^',
                'Shift':'+',
                'Alt':'!',
                'Win':'#',
                'R':'>',
                'L':'<',
            }
            for k,v in function_key_dict.items():
                function_key_name=function_key_name.replace(k,v)
            com_str+=function_key_name

        elif block_elt.attrs['type'] in ["normal_key","special_key"]:
            field_elt=FindCurrent(block_elt,'field')
            function_key_name=field_elt.text
            com_str+=function_key_name

        elif block_elt.attrs['type']=="return":
            com_str+='Return'

        elif block_elt.attrs['type']=="block_input":
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt,Indentation=False)
            com_str+=f"BlockInput, On\n{statement_do_str}BlockInput, Off\n"
        
        #endregion 按鍵Blockly

        #region 熱字串Blockly
        elif block_elt.attrs['type'] in ["hotstring","hotstring_advanced"]:
            #獲取縮寫元素
            value_abb_elt=FindCurrent(block_elt,'value[name="ABB"]')
            value_abb_str,value_abb_comment=AHK_value(value_abb_elt)
            value_abb_str=value_abb_str[1:-1] #去除冒號
            com_str+=value_abb_comment
            #獲取展開文字元素
            value_text_elt=FindCurrent(block_elt,'value[name="TEXT"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt)
            #去除冒號(只針對文字進行去除，不針對變量或函式)
            if value_text_str[0]==value_text_str[-1]=='"':
                value_text_str=value_text_str[1:-1] 
            com_str+=value_text_comment
            #獲取熱字串設定元素
            hotstring_setting_str=""
            expand_raw_text_bool=False
            statement_setting_elt=FindCurrent(block_elt,'statement[name="SETTING"]')
            if statement_setting_elt:
                hotstringSetting_dict={
                    "hotstringSetting_autoExpaned":"*",
                    "hotstringSetting_dontFireEndKey":"o",
                    "hotstringSetting_caseSensitive":"c",
                    "hotstringSetting_expanedInWrods":"?",
                }
                block_hotstringSetting_elt_list=statement_setting_elt.select('block')
                for block_hotstringSetting_elt in block_hotstringSetting_elt_list:
                    if block_hotstringSetting_elt.attrs['type']!="hotstringSetting_rawText":
                        hotstring_setting_symbol=hotstringSetting_dict[block_hotstringSetting_elt.attrs['type']]
                        hotstring_setting_str+=hotstring_setting_symbol
                    else:
                        expand_raw_text_bool=True
            #若要展開的文字元素不是文字(例如變數或函式返回值)，則換至下一行使用SendInput TEXT
            if value_text_elt and FindCurrent(value_text_elt,'block') and FindCurrent(value_text_elt,'block').attrs['type']!="text":
                com_str+=f':{hotstring_setting_str}:{value_abb_str}::\nSendInput % "{{TEXT}}" . {value_text_str}\nReturn\n'
            else:
                com_str+=f':{hotstring_setting_str}:{value_abb_str}::{f"{{TEXT}}"*expand_raw_text_bool}{value_text_str}\n'
        
        elif block_elt.attrs['type']=="hotstring_do":
            #獲取縮寫元素
            value_abb_elt=FindCurrent(block_elt,'value[name="ABB"]')
            value_abb_str,value_abb_comment=AHK_value(value_abb_elt)
            value_abb_str=value_abb_str[1:-1] #去除冒號
            com_str+=value_abb_comment
            #獲取執行內容元素
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt,for_hotkey=True)
            #獲取熱字串設定元素
            hotstring_setting_str=""
            statement_setting_elt=FindCurrent(block_elt,'statement[name="SETTING"]')
            if statement_setting_elt:
                #獲取熱字串設定元素中的註解
                comment_setting_elt_list=statement_setting_elt.select('comment')
                for comment_setting_elt in comment_setting_elt_list:
                    com_str+=Comment(comment_setting_elt.parent)
                hotstringSetting_dict={
                    "hotstringSetting_autoExpaned":"*",
                    "hotstringSetting_dontFireEndKey":"o",
                    "hotstringSetting_caseSensitive":"c",
                    "hotstringSetting_expanedInWrods":"?",
                }
                block_hotstringSetting_elt_list=statement_setting_elt.select('block')
                for block_hotstringSetting_elt in block_hotstringSetting_elt_list:
                    if block_hotstringSetting_elt.attrs['type']!="hotstringSetting_rawText":
                        hotstring_setting_symbol=hotstringSetting_dict[block_hotstringSetting_elt.attrs['type']]
                        hotstring_setting_str+=hotstring_setting_symbol

            com_str+=f':{hotstring_setting_str}:{value_abb_str}::{statement_do_str}\n'

        #endregion 熱字串Blockly
        
        #region 動作Blockly
        
        elif block_elt.attrs['type']=="open":
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'Run % {value_str}\n'

        elif block_elt.attrs['type']=="win_activate":
            #獲取要顯示的標題
            value_title_elt=FindCurrent(block_elt,'value[name="title"]')
            value_title_str,value_title_comment=AHK_value(value_title_elt,get_all_comment=True)
            com_str+=value_title_comment

            com_str+='\n'.join([
                f'WinActivate % {value_title_str}\n',
            ])


        elif block_elt.attrs['type']=="run_or_active":
            #獲取要執行的程式
            value_elt=FindCurrent(block_elt,'value[name="run"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            #獲取要顯示的標題
            value_title_elt=FindCurrent(block_elt,'value[name="title"]')
            value_title_str,value_title_comment=AHK_value(value_title_elt,get_all_comment=True)
            com_str+=value_title_comment

            com_str+='\n'.join([
                f'IfWinExist % {value_title_str}',
                f'{{',
                f'{TAB_SPACE}IfWinNotActive % {value_title_str}',
                f'{TAB_SPACE}{TAB_SPACE}WinActivate',
                f'}}',
                f'else',
                f'{{',
                f'{TAB_SPACE}Run % {value_str}',
                f'{TAB_SPACE}WinWait % {value_title_str}',
                f'{TAB_SPACE}WinActivate',
                f'}}\n',
            ])

        elif block_elt.attrs['type']=="file_recycle_empty":
            com_str+='FileRecycleEmpty\n'

        elif block_elt.attrs['type']=="reload":
            com_str+='Reload\n'

        elif block_elt.attrs['type']=="msgbox":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment

            com_str+=f"Msgbox % {value_str}\n"

        elif block_elt.attrs['type']=="traytip":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment

            com_str+=f"TrayTip,,% {value_str}\n"

        elif block_elt.attrs['type']=="send_text":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'SendInput % "{{TEXT}}" . {value_str}\n'

        elif block_elt.attrs['type']=="set_clipboard":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'Clipboard := {value_str}\n'

        elif block_elt.attrs['type']=="close_process":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=f'Process, Close, {field_elt.text}\n'

        elif block_elt.attrs['type']=="sleep":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            com_str+=f'Sleep % {value_str}\n'

        elif block_elt.attrs['type']=="shutdown":
            #獲取動作
            field_action_elt=FindCurrent(block_elt,'field[name="action"]')
            field_action_str=field_action_elt.text
            #獲取是否強制執行
            field_force_elt=FindCurrent(block_elt,'field[name="force"]')
            field_force_str=field_force_elt.text            
            #若為Shutdown語法 (登出/關機/重新啟動)
            if field_action_str in ["logout","shutdown","restart"]:
                action_int=0 if field_action_str=="logout" else 1 if field_action_str=="shutdown" else 2
                force_int=4 if field_force_str=="TRUE" else 0
                com_str+=f"Shutdown, {action_int+force_int}\n"
            #若為DllCall語法 (睡眠/休眠)
            elif field_action_str in ["sleep","deepsleep"]:
                var_int=0 if field_action_str=="sleep" else 1
                com_str+=f'DllCall("PowerProf\\SetSuspendState", "int", {var_int}, "int", 0, "int", 0,)\n'
            else:
                com_str+='Run rundll32.exe user32.dll`,LockWorkStation\n'

        elif block_elt.attrs['type']=="paste_text":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            com_str+='\n'.join([
                'clipboard_save := clipboard',
                'clipboard:=',
                f'clipboard:={value_str}',
                'ClipWait',
                'Send ^v',
                'Sleep 100',
                'clipboard = %clipboard_save%\n',
            ])

        elif block_elt.attrs['type']=="inputbox":
            #獲取變數名稱
            field_var_elt=FindCurrent(block_elt,'field[name="NAME"]')
            field_var_str=field_var_elt.text
            #獲取視窗寬度
            field_w_elt=FindCurrent(block_elt,'field[name="w"]')
            field_w_str=field_w_elt.text
            #獲取視窗高度
            field_h_elt=FindCurrent(block_elt,'field[name="h"]')
            field_h_str=field_h_elt.text
            #獲取標題文字
            value_title_elt=FindCurrent(block_elt,'value[name="title"]')
            value_title_str,value_title_comment=AHK_value(value_title_elt,get_all_comment=True)
            com_str+=value_title_comment
            #獲取內容文字
            value_text_elt=FindCurrent(block_elt,'value[name="text"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt,get_all_comment=True)
            com_str+=value_text_comment
            #輸出程式碼
            com_str+='\n'.join([
                f'__title := {value_title_str}',
                f'__text := {value_text_str}',
                f'InputBox, {field_var_str},%__title%,%__text%,,{field_w_str},{field_h_str}\n',
            ])

        elif block_elt.attrs['type']=="msgbox_yesorno":
            #獲取標題文字
            value_title_elt=FindCurrent(block_elt,'value[name="title"]')
            value_title_str,value_title_comment=AHK_value(value_title_elt,get_all_comment=True)
            com_str+=value_title_comment
            #獲取內容文字
            value_text_elt=FindCurrent(block_elt,'value[name="text"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt,get_all_comment=True)
            com_str+=value_text_comment
            #獲取按下是之後執行的動作
            statement_yes_elt=FindCurrent(block_elt,'statement[name="yes"]')
            statement_yes_str=AHK_statement(statement_yes_elt)
            #獲取按下是之後執行的動作
            statement_no_elt=FindCurrent(block_elt,'statement[name="no"]')
            statement_no_str=AHK_statement(statement_no_elt)
            #輸出程式碼
            com_str+='\n'.join([
                f'__title := {value_title_str}',
                f'__text := {value_text_str}',
                f'MsgBox, 4,%__title%,%__text%',
                f'IfMsgBox Yes',
                f'{{',
                f'{statement_yes_str}}}',
                f'else',
                f'{{',
                f'{statement_no_str}}}\n',
            ])
    


        #endregion 動作Blockly

        #region 物件Blockly

        #剪貼簿內容
        elif block_elt.attrs['type']=="clipboard":
            #尋找該積木是否在「貼上文字」的積木之下
            under_pasteText_block_bool=None
            block_elt=block_elt.parent
            while block_elt.tagName!="XML":
                if block_elt.tagName=="BLOCK" and block_elt.attrs['type']=="paste_text":
                    under_pasteText_block_bool=True
                block_elt=block_elt.parent
            #若是，則使用clipboard_save作為該積木的值
            if under_pasteText_block_bool:
                com_str+='clipboard_save'
            #若否，則使用Clipboard作為該積木的值
            else:
                com_str+='Clipboard'

        #目錄、檔案、網頁
        elif block_elt.attrs['type'] in ["filepath","dirpath","webpage"]:
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            field_str=field_elt.text
            #若為網頁，則需要替換特殊字元
            if block_elt.attrs['type']=="webpage":
                field_str=field_str.replace("%","`%").replace(",","`,")
            #若路徑有空白，就使用三個引號夾起
            if " " in field_str:
                com_str+=f'"""{field_str}"""'
            #若路徑沒有空白，就使用一個引號夾起
            else:
                com_str+=f'"{field_str}"'
        
        #文字
        elif block_elt.attrs['type']=="text":
            field_elt=FindCurrent(block_elt,'field')
            #替換特殊字元文字
            field_elt_str=field_elt.text.replace('`','``').replace('"','""')
            if field_elt:
                com_str+=f'"{field_elt_str}"'

        #合併文字
        elif block_elt.attrs['type']=="text_join":
            mutation_elt=FindCurrent(block_elt,"mutation")
            mutation_items_int=int(mutation_elt.attrs['items'])
            value_str_list=[]
            for i_item in range(mutation_items_int):
                value_elt=FindCurrent(block_elt,f'value[name="ADD{i_item}"]')
                value_str,value_comment=AHK_value(value_elt)
                value_str_list.append(value_str)
            
            value_str_list_str=" . ".join(value_str_list)
            com_str+=value_str_list_str

        #替換文字
        elif block_elt.attrs['type']=="str_replace":
            #獲取輸入的文字
            value_text_elt=FindCurrent(block_elt,'value[name="text"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt,get_all_comment=True)
            com_str+=value_text_comment
            #獲取搜尋的文字
            value_subs_elt=FindCurrent(block_elt,'value[name="subs"]')
            value_subs_str,value_subs_comment=AHK_value(value_subs_elt,get_all_comment=True)
            com_str+=value_subs_comment
            #獲取替換成的文字
            value_to_elt=FindCurrent(block_elt,'value[name="to"]')
            value_to_str,value_to_comment=AHK_value(value_to_elt,get_all_comment=True)
            com_str+=value_to_comment

            com_str+=f'StrReplace({value_text_str},{value_subs_str},{value_to_str})'

        #內建程式變量
        elif block_elt.attrs['type']=="built_in_program":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_program_dict={
                    "notepad":'"Notepad.exe"',
                    "mspaint":'"mspaint.exe"',
                    "calc":' windir . "\system32\calc.exe"',
                    "SnippingTool":' windir . "\system32\SnippingTool.exe"',
                    "cmd":' windir . "\system32\cmd.exe"',
                    "ahkfile":'A_ScriptFullPath',
                    "ahkexe":'A_AhkPath',
                }
                field_str=built_in_program_dict[field_elt.text]
                com_str+=f'{field_str}'

        #內建路徑變量
        elif block_elt.attrs['type']=="built_in_dirpath":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_program_dict={
                    "desktop":'A_Desktop',
                    "mydocuments":'A_MyDocuments',
                    "startup":'A_Startup',
                    "temp":'A_Temp',
                    "windows":'A_WinDir',
                    "ahkfilepath":'A_ScriptDir',
                }
                field_str=built_in_program_dict[field_elt.text]
                com_str+=f'{field_str}'

        elif block_elt.attrs['type']=="built_in_webpage":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_webpage_dict={
                    "google":'https://www.google.com',
                    "youtube":'https://www.youtube.com',
                    "facebook":'https://www.facebook.com',
                    "baidu":'https://www.baidu.com/',
                    "wikipedia":'https://zh.wikipedia.org',
                    "pchome":"https://www.pchome.com.tw",
                    "yahoo":"https://yahoo.com",
                    "googlemap":"https://www.google.com.tw/maps",
                    "ahk":"https://www.autohotkey.com",
                    "ahkblockly":"https://sites.google.com/view/ahktool/ahkblockly",
                }
                field_str=built_in_webpage_dict[field_elt.text]
                com_str+=f'"{field_str}"'

        #用主程式開啟檔案
        elif block_elt.attrs['type']=="open_with_main_program":
            #獲取主程式積木
            value_mainProgram_elt=FindCurrent(block_elt,'value[name="main_program"]')
            value_mainProgram_str,value_mainProgram_comment=AHK_value(value_mainProgram_elt,get_all_comment=True)
            com_str+=value_mainProgram_comment
            #獲取檔案積木
            value_file_elt=FindCurrent(block_elt,'value[name="file"]')
            value_file_str,value_file_comment=AHK_value(value_file_elt,get_all_comment=True)
            com_str+=value_file_comment

            com_str+=f'{value_mainProgram_str} . " " . {value_file_str}'

        #路徑合併
        elif block_elt.attrs['type']=="path_combined":
            value_mainPath_elt=FindCurrent(block_elt,'value[name="main_path"]')
            value_mainPath_str,value_mainPath_comment=AHK_value(value_mainPath_elt)
            com_str+=value_mainPath_comment

            value_subPath_elt=FindCurrent(block_elt,'value[name="sub_path"]')
            value_subPath_str,value_subPath_comment=AHK_value(value_subPath_elt)
            com_str+=value_subPath_comment
            
            com_str+=f'{value_mainPath_str} . "\\" . {value_subPath_str}'

        #數字
        elif block_elt.attrs['type']=="math_number":
            field_elt=FindCurrent(block_elt,'field[name="NUM"]')
            com_str+=field_elt.text.strip()

        #數學算式
        elif block_elt.attrs['type']=="math_arithmetic":
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            field_op_str_dict={
                'ADD':'+',
                'MINUS':'-',
                'MULTIPLY':'*',
                'DIVIDE':'/',
                'POWER':'**',
            }
            field_op_str=field_op_str_dict[field_op_elt.text]

            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,_=AHK_value(value_a_elt)
            
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,_=AHK_value(value_b_elt)

            com_str+=f'({value_a_str}{field_op_str}{value_b_str})'

        #數學函數
        elif block_elt.attrs['type'] in ["math_function","math_function2"]:
            #獲取數字積木
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "0"
            com_str+=value_comment
            #獲取數學函數名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            #輸出語法
            com_str+=f'{field_elt.text}({value_str})'

        #數學常數
        elif block_elt.attrs['type']=="math_constant2":
            #獲取數學常數名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            if field_elt.text=="pi":
                com_str+='4*atan(1)'
            elif field_elt.text=="e":
                com_str+='exp(1)'
            elif field_elt.text=="golden_ratio":
                com_str+='(1+sqrt(5))/2'
        
        #四捨五入
        elif block_elt.attrs['type']=="math_round":
            #獲取數字積木
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "0"
            com_str+=value_comment
            #獲取位數積木
            value_digit_elt=FindCurrent(block_elt,'value[name="digit"]')
            value_digit_str,value_digit_comment=AHK_value(value_digit_elt,get_all_comment=True)
            value_digit_str=value_digit_str if value_digit_str else "0"
            com_str+=value_digit_comment
            #
            if value_digit_str=="0":
                com_str+=f'round({value_str})'
            else:
                com_str+=f'round({value_str},{value_digit_str})'

        #取餘數或商數
        elif block_elt.attrs['type']=="math_mod":
            #獲取被除數數字積木
            value_a_elt=FindCurrent(block_elt,'value[name="a"]')
            value_a_str,value_a_comment=AHK_value(value_a_elt,get_all_comment=True)
            value_a_str=value_a_str if value_a_str else "0"
            com_str+=value_a_comment
            #獲取除數數字積木
            value_b_elt=FindCurrent(block_elt,'value[name="b"]')
            value_b_str,value_b_comment=AHK_value(value_b_elt,get_all_comment=True)
            value_b_str=value_b_str if value_b_str else "1"
            com_str+=value_b_comment
            #獲取是取餘數或商數
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            if field_elt.text=="商數":
                com_str+=f'{value_a_str}//{value_b_str}'
            else:
                com_str+=f'Mod({value_a_str}, {value_b_str})'

        #取隨機數
        elif block_elt.attrs['type']=="math_random":
            #獲取最小值數字積木
            value_min_elt=FindCurrent(block_elt,'value[name="min"]')
            value_min_str,value_min_comment=AHK_value(value_min_elt,get_all_comment=True)
            value_min_str=value_min_str if value_min_str else "0"
            com_str+=value_min_comment
            #獲取最大值數字積木
            value_max_elt=FindCurrent(block_elt,'value[name="max"]')
            value_max_str,value_max_comment=AHK_value(value_max_elt,get_all_comment=True)
            value_max_str=value_max_str if value_max_str else "0"
            com_str+=value_max_comment
            #獲取變數名稱
            field_var_elt=FindCurrent(block_elt,f'field[name="NAME"]')
            value_var_str=field_var_elt.text
            #獲取亂數類型
            field_type_elt=FindCurrent(block_elt,f'field[name="type"]')
            if field_type_elt.text=="int":
                com_str+=f'Random, {value_var_str}, ceil({value_min_str}), floor({value_max_str})\n'
            else:
                com_str+=f'Random, {value_var_str}, {value_min_str}*1.0, {value_max_str}*1.0\n'

        #日期時間
        elif block_elt.attrs['type']=="built_in_time":
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            built_in_time_dict={
                "year":"A_YYYY",
                "month":"A_MM",
                "day":"A_DD",
                "wday":"(A_WDay=1 ? 7 : A_WDay-1)",
                "hour":"A_Hour",
                "min":"A_Min",
                "sec":"A_Sec",
            }
            com_str+=built_in_time_dict[field_elt.text]

        elif block_elt.attrs['type']=="built_in_wday_zh":
            com_str+='Array("日","一","二","三","四","五","六")[A_WDay]'


        #endregion 物件Blockly
        
        #region 模擬鍵盤Blockly
        elif block_elt.attrs['type']=="send_key":
            hotkey_str=""

            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取功能鍵
            block_functionKey_elt_list=block_sendKey_elt.select('block[type="function_key"]')
            for block_functionKey_elt in block_functionKey_elt_list:
                functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                hotkey_str+=functionKey_str
                com_str+=functionKey_comment
            #獲取一般鍵(將英文字母按鍵名稱降為小寫)
            block_normalKey_elt_list=block_sendKey_elt.select('block[type="normal_key"]')
            block_normalKey_elt_list.extend(block_sendKey_elt.select('block[type="special_key"]'))
            for block_normalKey_elt in block_normalKey_elt_list:
                normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                hotkey_str+=(normalKey_str.lower() if block_normalKey_elt.attrs['type']=="normal_key" else f"{{{normalKey_str}}}")
                com_str+=normalKey_comment
            
            com_str+=f'Send, {hotkey_str}\n'

        elif block_elt.attrs['type']=="send_keys":
            hotkey_str=""

            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取一般連續鍵
            field_elt=FindCurrent(block_elt,'field')
            
            com_str+=f'Send, {field_elt.text}\n'

        elif block_elt.attrs['type']=="send_key_times":
            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取功能鍵
            functionKey_all_str=""
            block_functionKey_elt_list=block_sendKey_elt.select('block[type="function_key"]')
            for block_functionKey_elt in block_functionKey_elt_list:
                functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                functionKey_all_str+=functionKey_str
                com_str+=functionKey_comment
            #獲取一般鍵(將英文字母按鍵名稱降為小寫)，此處應只有獲取一個元素
            block_normalKey_elt_list=block_sendKey_elt.select('block[type="normal_key"]')
            block_normalKey_elt_list.extend(block_sendKey_elt.select('block[type="special_key"]'))
            for block_normalKey_elt in block_normalKey_elt_list:
                normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                if block_normalKey_elt.attrs['type']=="normal_key":
                    normalKey_str=normalKey_str.lower()
                com_str+=normalKey_comment

            #獲取次數元素
            value_times_elt=FindCurrent(block_elt,'value[name="TIMES"]')
            value_times_str,value_times_comment=AHK_value(value_times_elt)
            com_str+=value_times_comment
            
            com_str+=f'Send, {functionKey_all_str}{{{normalKey_str} {value_times_str}}}\n'

        #等待功能鍵釋放
        elif block_elt.attrs['type']=="key_wait":
            #獲取功能鍵
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #對於等待Win按鍵釋放，需要兩行程式碼寫完
            if value_str=="Win":
                com_str+=f'KeyWait, LWin\nKeyWait, RWin\n'
            else:
                com_str+=f'KeyWait, {value_str}\n'

        #按著功能鍵
        elif block_elt.attrs['type']=="key_pressing":
            #獲取功能鍵
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #獲取執行元素
            statement_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_str=AHK_statement(statement_elt,Indentation=False) #不要將執行式縮排
            #輸出程式碼
            com_str=f'Send {{{value_str} Down}}\n{statement_str}Send {{{value_str} Up}}\n'

        #按著功能鍵
        elif block_elt.attrs['type'] in ["key_down","key_up"]:
            # print(1)
            #獲取功能鍵
            value_elt=FindCurrent(block_elt,'value',get_one=True)
            # print(2)
            value_str,value_comment=AHK_value(value_elt)
            # print(3)
            com_str+=value_comment
            # print(value_str)
            # print(block_elt.attrs['type'])
            # print(block_elt.attrs['type'].replace('key_').upper())
            
            #輸出程式碼
            com_str+=f"Send {{{value_str} {block_elt.attrs['type'].replace('key_','').upper()}}}\n"



        #endregion 模擬鍵盤Blockly

        #region 模擬滑鼠Blockly

        #coord_mode
        elif block_elt.attrs['type']=="coord_mode":
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            coord_mode_str=field_name_elt.text
            coord_mode_str=coord_mode_str[0].upper()+coord_mode_str[1:]
            com_str+=f'CoordMode, Mouse , {coord_mode_str}\n'

        #點擊(x,y)
        elif block_elt.attrs['type']=="click_x_y":
            value_x_elt=FindCurrent(block_elt,f'value[name="X"]')
            value_x_str,value_x_comment=AHK_value(value_x_elt)
            com_str+=value_x_comment

            value_y_elt=FindCurrent(block_elt,f'value[name="Y"]')
            value_y_str,value_y_comment=AHK_value(value_y_elt)
            com_str+=value_y_comment

            value_times_elt=FindCurrent(block_elt,f'value[name="TIMES"]')
            value_times_str,value_times_comment=AHK_value(value_times_elt)
            com_str+=value_times_comment
           
            com_str+="\n".join([
                f"__ClickX:={value_x_str}",
                f"__ClickY:={value_y_str}",
                f"__ClickTimes:={value_times_str}",
                f"Click %__ClickX%, %__ClickY%, %__ClickTimes%\n",
            ])
        
        elif block_elt.attrs['type']=="mouse_get_pos":
            field_posX_elt=FindCurrent(block_elt,f'field[name="posX"]')
            value_posX_str=field_posX_elt.text

            field_posY_elt=FindCurrent(block_elt,f'field[name="posY"]')
            value_posY_str=field_posY_elt.text

            com_str+=f'MouseGetPos, {value_posX_str}, {value_posY_str}\n'
        
        
        #endregion 模擬滑鼠Blockly

        #region 偵測圖片Blockly

        #偵測像素
        elif block_elt.attrs['type']=="get_pixel_pos":
            #獲取偵測圖片設定區塊
            statement_setting_elt=FindCurrent(block_elt,'statement[name="get_pixel_pos_setting"]')
            statement_setting_elt_comment=Comment(statement_setting_elt,get_all_comment=True)
            com_str+=statement_setting_elt_comment

            #獲取像素顏色(RGB)
            block_pixelRGBColor_elt=statement_setting_elt.select_one('block[type="pixel_rgb_color"]')
            #獲取像素顏色(R)
            value_R_elt=FindCurrent(block_pixelRGBColor_elt,'value[name="R"]') if block_pixelRGBColor_elt else None
            value_R_elt_str,value_R_elt_comment=AHK_value(value_R_elt) if value_R_elt else ('0','')
            value_R_elt_int=int(value_R_elt_str)
            value_R_elt_int=max(0,min(value_R_elt_int,255))
            #獲取像素顏色(G)
            value_G_elt=FindCurrent(block_pixelRGBColor_elt,'value[name="R"]') if block_pixelRGBColor_elt else None
            value_G_elt_str,value_G_elt_comment=AHK_value(value_G_elt) if value_G_elt else ('0','')
            value_G_elt_int=int(value_G_elt_str)
            value_G_elt_int=max(0,min(value_G_elt_int,255))
            #獲取像素顏色(B)
            value_B_elt=FindCurrent(block_pixelRGBColor_elt,'value[name="R"]') if block_pixelRGBColor_elt else None
            value_B_elt_str,value_B_elt_comment=AHK_value(value_B_elt) if value_B_elt else ('0','')
            value_B_elt_int=int(value_B_elt_str)
            value_B_elt_int=max(0,min(value_B_elt_int,255))
            #根據RGB像素顏色產生 ColorID
            value_RGB_elt_str=f'{value_R_elt_int:02x}{value_G_elt_int:02x}{value_B_elt_int:02x}'

            #獲取像素顏色(ColorID)
            block_pixelColorId_elt=statement_setting_elt.select_one('block[type="pixel_color_id"]')
            field_colorId_elt=FindCurrent(block_pixelColorId_elt,'field[name="ColorID"]')
            field_colorId_str=field_colorId_elt.text if field_colorId_elt else value_RGB_elt_str if block_pixelRGBColor_elt else "FFFFFF"

            #檢查偵測像素積木內是否有指定像素顏色，沒有的話就跳出警示訊息，並預設使用白色(FFFFFF)進行偵測
            if (not block_pixelColorId_elt) and (not block_pixelRGBColor_elt):
                alert("偵測像素積木內沒有指定像素顏色\n請填入RGB積木或色碼積木")

            #獲取搜尋範圍
            block_image_search_area_elt=statement_setting_elt.select_one('block[type="pixel_search_area"]')
            #獲取搜尋範圍X
            value_x_elt=FindCurrent(block_image_search_area_elt,'value[name="X"]') if block_image_search_area_elt else None
            value_x_elt_str,value_x_elt_comment=AHK_value(value_x_elt) if value_x_elt else ("0","")
            #獲取搜尋範圍Y
            value_y_elt=FindCurrent(block_image_search_area_elt,'value[name="Y"]') if block_image_search_area_elt else None
            value_y_elt_str,value_y_elt_comment=AHK_value(value_y_elt) if value_y_elt else ("0","")
            #獲取搜尋範圍W
            value_w_elt=FindCurrent(block_image_search_area_elt,'value[name="W"]') if block_image_search_area_elt else None
            value_w_elt_str,value_w_elt_comment=AHK_value(value_w_elt) if value_w_elt else ("0","")
            if not value_w_elt:func_dict_key_set.update(['screen_width'])
            #獲取搜尋範圍H
            value_h_elt=FindCurrent(block_image_search_area_elt,'value[name="H"]') if block_image_search_area_elt else None
            value_h_elt_str,value_h_elt_comment=AHK_value(value_h_elt) if value_h_elt else ("0","")
            if not value_h_elt:func_dict_key_set.update(['screen_height'])
            
            #獲取posX變量名稱
            field_posXVar_elt=FindCurrent(block_elt,'field[name="pos_x"]')
            posXVar_str=field_posXVar_elt.text
            #獲取posY變量名稱
            field_posYVar_elt=FindCurrent(block_elt,'field[name="pos_y"]')
            posYVar_str=field_posYVar_elt.text
            #獲取找到圖片後執行動作
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            #獲取找不到圖片後執行動作
            statement_elseDo_elt=FindCurrent(block_elt,'statement[name="ELSE_DO"]')
            statement_elseDo_str=AHK_statement(statement_elseDo_elt)
            # statement_elseDo_str=statement_elseDo_str.replace("\n","\n"+TAB_SPACE) #二次縮排
            com_str+='\n'.join([
                'CoordMode Pixel',
                ';搜尋像素點',
                f'PixelSearch, __FoundX, __FoundY, {value_x_elt_str}, {value_y_elt_str}, {value_w_elt_str}, {value_h_elt_str}, 0x{field_colorId_str},,Fast RGB',
                'CoordMode Mouse',
                ';獲取像素點座標',
                f'{posXVar_str}:=__FoundX',
                f'{posYVar_str}:=__FoundY',
                'if (ErrorLevel=0) {',
                f'{statement_do_str}'+''+'} else {',
                f'{statement_elseDo_str}'+'}\n',
            ])

        #偵測圖片
        elif block_elt.attrs['type']=="get_picture_pos_ver200419":
            #獲取偵測圖片設定區塊
            statement_setting_elt=FindCurrent(block_elt,'statement[name="get_picture_pos_setting"]')
            statement_setting_elt_comment=Comment(statement_setting_elt,get_all_comment=True)
            com_str+=statement_setting_elt_comment

            #獲取圖片路徑
            block_imgFilepath_elt=statement_setting_elt.select_one('block[type="image_filepath"]')
            value_imgFilepath_elt=FindCurrent(block_imgFilepath_elt,'value[name="NAME"]') if block_imgFilepath_elt else None
            value_imgFilepath_str,value_imgFilepath_comment=AHK_value(value_imgFilepath_elt) if value_imgFilepath_elt else ("","")

            #獲取搜尋範圍
            block_image_search_area_elt=statement_setting_elt.select_one('block[type="image_search_area"]')
            #獲取搜尋範圍X
            value_x_elt=FindCurrent(block_image_search_area_elt,'value[name="X"]') if block_image_search_area_elt else None
            value_x_elt_str,value_x_elt_comment=AHK_value(value_x_elt) if value_x_elt else ("0","")
            #獲取搜尋範圍Y
            value_y_elt=FindCurrent(block_image_search_area_elt,'value[name="Y"]') if block_image_search_area_elt else None
            value_y_elt_str,value_y_elt_comment=AHK_value(value_y_elt) if value_y_elt else ("0","")
            #獲取搜尋範圍X
            value_w_elt=FindCurrent(block_image_search_area_elt,'value[name="W"]') if block_image_search_area_elt else None
            value_w_elt_str,value_w_elt_comment=AHK_value(value_w_elt) if value_w_elt else ("0","")
            if not value_w_elt:func_dict_key_set.update(['screen_width'])
            #獲取搜尋範圍X
            value_h_elt=FindCurrent(block_image_search_area_elt,'value[name="H"]') if block_image_search_area_elt else None
            value_h_elt_str,value_h_elt_comment=AHK_value(value_h_elt) if value_h_elt else ("0","")
            if not value_h_elt:func_dict_key_set.update(['screen_height'])
            
            #獲取posX變量名稱
            field_posXVar_elt=FindCurrent(block_elt,'field[name="pos_x"]')
            posXVar_str=field_posXVar_elt.text
            #獲取posY變量名稱
            field_posYVar_elt=FindCurrent(block_elt,'field[name="pos_y"]')
            posYVar_str=field_posYVar_elt.text
            #獲取找到圖片後執行動作
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            statement_do_str=statement_do_str.replace("\n","\n"+TAB_SPACE) #二次縮排
            #獲取找不到圖片後執行動作
            statement_elseDo_elt=FindCurrent(block_elt,'statement[name="ELSE_DO"]')
            statement_elseDo_str=AHK_statement(statement_elseDo_elt)
            statement_elseDo_str=statement_elseDo_str.replace("\n","\n"+TAB_SPACE) #二次縮排
            com_str+='\n'.join([
                f'__ImageFilePath:={value_imgFilepath_str}',
                f'gui,add,picture,hwnd__mypic,%__ImageFilePath%',
                'if FileExist(__ImageFilePath){',
                TAB_SPACE+'controlgetpos,,,__img_w,__img_h,,ahk_id %__mypic%',
                TAB_SPACE+'CoordMode Pixel',
                TAB_SPACE+';搜尋圖片',
                TAB_SPACE+f'ImageSearch, __FoundX, __FoundY, {value_x_elt_str}, {value_y_elt_str}, {value_w_elt_str}, {value_h_elt_str},%__ImageFilePath%',
                TAB_SPACE+'CoordMode Mouse',
                TAB_SPACE+';獲取圖片中心座標',
                TAB_SPACE+f'{posXVar_str}:=__FoundX + __img_w/2',
                TAB_SPACE+f'{posYVar_str}:=__FoundY + __img_h/2',
                TAB_SPACE+'if (ErrorLevel=0) {',
                TAB_SPACE+f'{statement_do_str}'+''+'} else {',
                TAB_SPACE+f'{statement_elseDo_str}'+''+'}',
                '} else {',
                TAB_SPACE+'Msgbox % "圖片路徑不存在"',
                '}\n',
            ])


        elif block_elt.attrs['type']=="get_picture_pos_ver200406":
            #獲取設值blockly
            value_imgFilepath_elt=FindCurrent(block_elt,'value[name="image_filepath"]')
            value_imgFilepath_str,value_imgFilepath_comment=AHK_value(value_imgFilepath_elt)
            #獲取posX變量名稱
            field_posXVar_elt=FindCurrent(block_elt,'field[name="pos_x"]')
            posXVar_str=field_posXVar_elt.text
            #獲取posY變量名稱
            field_posYVar_elt=FindCurrent(block_elt,'field[name="pos_y"]')
            posYVar_str=field_posYVar_elt.text
            #獲取找到圖片後執行動作
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            #獲取找不到圖片後執行動作
            statement_elseDo_elt=FindCurrent(block_elt,'statement[name="ELSE_DO"]')
            statement_elseDo_str=AHK_statement(statement_elseDo_elt)
            com_str+='\n'.join([
                f'__ImageFilePath:={value_imgFilepath_str}',
                f'gui,add,picture,hwnd__mypic,%__ImageFilePath%',
                'if FileExist(__ImageFilePath){',
                TAB_SPACE+'controlgetpos,,,__img_w,__img_h,,ahk_id %__mypic%',
                TAB_SPACE+';獲取顯示器長寬',
                TAB_SPACE+'SysGet, VirtualWidth, 78',
                TAB_SPACE+'SysGet, VirtualHeight, 79',
                TAB_SPACE+'CoordMode Pixel',
                TAB_SPACE+';搜尋圖片',
                TAB_SPACE+'ImageSearch, __FoundX, __FoundY, 0, 0, VirtualWidth, VirtualHeight,%__ImageFilePath%',
                TAB_SPACE+'CoordMode Mouse',
                TAB_SPACE+';獲取圖片中心座標',
                TAB_SPACE+f'{posXVar_str}:=__FoundX + __img_w/2',
                TAB_SPACE+f'{posYVar_str}:=__FoundY + __img_h/2',
                TAB_SPACE+'if (ErrorLevel=0) {',
                TAB_SPACE+f'{statement_do_str}'+TAB_SPACE+'} else {',
                TAB_SPACE+f'{statement_elseDo_str}'+TAB_SPACE+'}',
                '} else {',
                TAB_SPACE+'Msgbox % "圖片路徑不存在"',
                '}\n',
            ])



        elif block_elt.attrs['type']=="get_picture_pos":
            #獲取圖片路徑
            field_imgFilepath_elt=FindCurrent(block_elt,'field[name="img_filepath"]')
            img_filepath_str=field_imgFilepath_elt.text
            #獲取posX變量名稱
            field_posXVar_elt=FindCurrent(block_elt,'field[name="pos_x"]')
            posXVar_str=field_posXVar_elt.text
            #獲取posY變量名稱
            field_posYVar_elt=FindCurrent(block_elt,'field[name="pos_y"]')
            posYVar_str=field_posYVar_elt.text
            #獲取找到圖片後執行動作
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            #獲取找不到圖片後執行動作
            statement_elseDo_elt=FindCurrent(block_elt,'statement[name="ELSE_DO"]')
            statement_elseDo_str=AHK_statement(statement_elseDo_elt)
            com_str+='\n'.join([
                f'__ImageFilePath:="{img_filepath_str}"',
                f'gui,add,picture,hwnd__mypic,%__ImageFilePath%',
                'if FileExist(__ImageFilePath){',
                TAB_SPACE+'controlgetpos,,,__img_w,__img_h,,ahk_id %__mypic%',
                TAB_SPACE+';獲取顯示器長寬',
                TAB_SPACE+'SysGet, VirtualWidth, 78',
                TAB_SPACE+'SysGet, VirtualHeight, 79',
                TAB_SPACE+'CoordMode Pixel',
                TAB_SPACE+';搜尋圖片',
                TAB_SPACE+'ImageSearch, __FoundX, __FoundY, 0, 0, VirtualWidth, VirtualHeight,%__ImageFilePath%',
                TAB_SPACE+'CoordMode Mouse',
                TAB_SPACE+';獲取圖片中心座標',
                TAB_SPACE+f'{posXVar_str}:=__FoundX + __img_w/2',
                TAB_SPACE+f'{posYVar_str}:=__FoundY + __img_h/2',
                TAB_SPACE+'if (ErrorLevel=0) {',
                TAB_SPACE+f'{statement_do_str}'+TAB_SPACE+'} else {',
                TAB_SPACE+f'{statement_elseDo_str}'+TAB_SPACE+'}',
                '} else {',
                TAB_SPACE+'Msgbox % "圖片路徑不存在"',
                '}\n',
            ])


        #endregion 偵測圖片Blockly

        #region 網頁操作
        elif "web_element_" in block_elt.attrs['type']:

            block_webAction_elt=block_elt
            
            #獲取連續的網頁操作blockly
            block_webAction_elt_list=[block_webAction_elt]
            while True:
                next_elt=FindCurrent(block_webAction_elt,'next')
                if next_elt:
                    block_webAction_elt=FindCurrent(next_elt,'block')
                    if "web_element_" in block_webAction_elt.attrs['type']:
                        block_webAction_elt_list.append(block_webAction_elt)
                    else:
                        #若循環到斷點(下一個積木不是網頁操作blockly)，就將block_elt退回到之前，給後面程式碼「#處理下一個block」章節處理
                        block_elt=block_webAction_elt.parent.parent
                        break
                else:
                    #若循環到斷點(沒有下一個積木了)，就將傳送當前的block_elt給後面程式碼「#處理下一個block」章節處理
                    block_elt=block_webAction_elt
                    break
            
            #print([block_webAction_elt.attrs['id'] for block_webAction_elt in block_webAction_elt_list])

            #逐個處理每個網頁操作blockly，匯出完整JS程式碼
            com_js_code_str=""
            for block_webAction_elt in block_webAction_elt_list:
                #獲取網頁元素的JS路徑
                if block_webAction_elt.attrs['type']!='web_element_alert':
                    #獲取網頁元素blockly
                    value_block_webElt_elt=FindCurrent(block_webAction_elt,'value[name="NAME"]')
                    #若沒有放網頁元素blockly，就跳過這個循環
                    if not value_block_webElt_elt:
                        continue
                    block_webElt_elt=FindCurrent(value_block_webElt_elt,'block[type="web_element"]')
                    #獲取網頁元素JS path
                    field_elt=FindCurrent(block_webElt_elt,'field[name="NAME"]')
                    #根據地址類型轉換元素地址文字
                    web_elt_JSpath_str=field_elt.text if FindCurrent(block_webElt_elt,f'field[name="elt_address"]').text=="js_path" else f'document.querySelector("{field_elt.text}")'
                #若為點擊
                if block_webAction_elt.attrs['type']=='web_element_click':
                    com_js_code_str+=f"{web_elt_JSpath_str}.click();\n"
                #若為聚焦
                elif block_webAction_elt.attrs['type']=='web_element_focus':
                    com_js_code_str+=f"{web_elt_JSpath_str}.focus();\n"
                #若為更改文字框內容
                elif block_webAction_elt.attrs['type']=='web_element_setValue':
                    #獲取設值blockly
                    value_toValue_elt=FindCurrent(block_webAction_elt,'value[name="to_value"]')
                    value_toValue_str,value_toValue_comment=AHK_value(value_toValue_elt)
                    com_str+=value_toValue_comment
                    com_js_code_str+=f'{web_elt_JSpath_str}.value={value_toValue_str};\n'
                #若為更改下拉選單
                elif block_webAction_elt.attrs['type']=='web_element_selectedindex':
                    #獲取設值blockly
                    value_toValue_elt=FindCurrent(block_webAction_elt,'value[name="to_value"]')
                    value_toValue_str,value_toValue_comment=AHK_value(value_toValue_elt)
                    com_str+=value_toValue_comment
                    com_js_code_str+=f'{web_elt_JSpath_str}.selectedIndex={value_toValue_str}-1;\n'
                #若為alert()
                elif block_webAction_elt.attrs['type']=='web_element_alert':
                    #獲取設值blockly
                    value_text_elt=FindCurrent(block_webAction_elt,'value[name="NAME"]')
                    value_text_str,value_text_comment=AHK_value(value_text_elt)
                    com_str+=value_text_comment
                    com_js_code_str+=f'alert({value_text_str});\n'


            
            #JS程式碼預處理 (將反斜線正常化)
            com_js_code_str=com_js_code_str.replace('\\','\\\\')

            #JS程式碼不為空
            if com_js_code_str:
                com_str+='\n'.join([
                    f'__JS程式碼=',
                    f'(',
                    f'{com_js_code_str}void(0);',
                    f')',
                    f'WinGetActiveTitle, __視窗標題',
                    f'if InStr(__視窗標題," - Google Chrome") {{',
                    f'{TAB_SPACE}BlockInput, On',
                    f'{TAB_SPACE}Send, ^l',
                    f'{TAB_SPACE}clipboard_save := clipboard',
                    f'{TAB_SPACE}clipboard:=',
                    f'{TAB_SPACE}clipboard:="_Javascript:" . __JS程式碼',
                    f'{TAB_SPACE}ClipWait',
                    f'{TAB_SPACE}Send ^v',
                    f'{TAB_SPACE}Sleep 100',
                    f'{TAB_SPACE}clipboard = %clipboard_save%',
                    f'{TAB_SPACE}Send, {{Home}}',
                    f'{TAB_SPACE}Send, {{Delete}}',
                    f'{TAB_SPACE}Send, {{Enter}}',
                    f'{TAB_SPACE}BlockInput, Off',
                    f'}} else {{',
                    f'{TAB_SPACE}Msgbox % "只有Google瀏覽器才可以執行該函式"',
                    f'}}\n',
                ])


        #endregion 網頁操作


        #region 函式Blockly

        elif block_elt.attrs['type']=="procedures_defnoreturn":
            #獲取函式名稱
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            function_name_str=field_name_elt.text
            #獲取變數列表
            arg_str_list=[]
            mutation_elt=FindCurrent(block_elt,'mutation')
            if mutation_elt:
                for arg_elt in mutation_elt.select('arg'):
                    arg_str_list.append(arg_elt.attrs['name'])
            arg_str=", ".join(arg_str_list)
            #獲取執行內容
            statement_elt=FindCurrent(block_elt,'statement[name="STACK"]')
            statement_str=AHK_statement(statement_elt)
            #若函式裡有使用螢幕寬高的機木，就補充螢幕寬高的全域宣告
            if block_elt.select_one('block[type="system_info_num"]'):
                statement_str=f'{TAB_SPACE}global VirtualHeight,VirtualWidth\n'+statement_str
            #輸出程式碼
            com_str+=f'{function_name_str}({arg_str}){{\n{statement_str}}}\n'

        elif block_elt.attrs['type']=="procedures_defreturn":
            #獲取函式名稱
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            function_name_str=field_name_elt.text
            #獲取變數列表
            arg_str_list=[]
            mutation_elt=FindCurrent(block_elt,'mutation')
            if mutation_elt:
                for arg_elt in mutation_elt.select('arg'):
                    arg_str_list.append(arg_elt.attrs['name'])
            arg_str=", ".join(arg_str_list)
            #獲取執行內容
            statement_elt=FindCurrent(block_elt,'statement[name="STACK"]')
            statement_str=AHK_statement(statement_elt)
            #獲取返回內容
            value_return_elt=FindCurrent(block_elt,'value[name="RETURN"]')
            value_return_str,value_return_comment=AHK_value(value_return_elt)
            value_return_str=TAB_SPACE + f'Return {value_return_str}\n'
            com_str+=value_return_comment
            #若函式裡有使用螢幕寬高的機木，就補充螢幕寬高的全域宣告
            if block_elt.select_one('block[type="system_info_num"]'):
                statement_str=f'{TAB_SPACE}global VirtualHeight,VirtualWidth\n'+statement_str
            #輸出程式碼
            com_str+=f'{function_name_str}({arg_str}){{\n{statement_str}{value_return_str}}}\n'
        

        elif block_elt.attrs['type']=="procedures_callnoreturn":
            #獲取函式名稱
            mutation_elt=block_elt.select_one('mutation')
            function_name_str=mutation_elt.attrs['name']
            #獲取變數列表
            arg_elt_list=mutation_elt.select('arg')
            arg_str_list=[]
            for i_arg in range(len(arg_elt_list)):
                #獲取參數數值
                value_arg_elt=FindCurrent(block_elt,f'value[name="ARG{i_arg}"]')
                value_arg_str,_=AHK_value(value_arg_elt)
                value_arg_str=value_arg_str if value_arg_str else ""
                #獲取參數名稱
                arg_elt=arg_elt_list[i_arg]
                arg_name_str=arg_elt.attrs['name']
                #生成「參數:=數值」表達式
                arg_str=f'{arg_name_str}:={value_arg_str}'
                arg_str_list.append(arg_str)
            arg_str_list_str=", ".join(arg_str_list)
            com_str+=f'{function_name_str}({arg_str_list_str})\n' #沒有return是執行式，所以要換行

        elif block_elt.attrs['type']=="procedures_callreturn":
            #獲取函式名稱
            mutation_elt=block_elt.select_one('mutation')
            function_name_str=mutation_elt.attrs['name']
            #獲取變數列表
            arg_elt_list=mutation_elt.select('arg')
            arg_str_list=[]
            for i_arg in range(len(arg_elt_list)):
                #獲取參數數值
                value_arg_elt=FindCurrent(block_elt,f'value[name="ARG{i_arg}"]')
                value_arg_str,_=AHK_value(value_arg_elt)
                value_arg_str=value_arg_str if value_arg_str else ""
                #獲取參數名稱
                arg_elt=arg_elt_list[i_arg]
                arg_name_str=arg_elt.attrs['name']
                #生成「參數:=數值」表達式
                arg_str=f'{arg_name_str}:={value_arg_str}'
                arg_str_list.append(arg_str)
            arg_str_list_str=", ".join(arg_str_list)
            
            com_str+=f'{function_name_str}({arg_str_list_str})' #有return東西會向左賦值，所以不用換行


        #endregion 函式Blockly

        #region 變數Blockly
        elif block_elt.attrs['type']=="variables_get":
            #獲取變數名稱(取代空白為底線)
            var_name=block_elt.select_one('field').text
            #轉換變數名稱為全形
            var_name=ToFullWidthString(var_name)
            com_str+=var_name

        elif block_elt.attrs['type']=="variables_set":
            #獲取變數名稱(取代空白為底線)
            field_elt=FindCurrent(block_elt,'field[name="VAR"]')
            var_name=field_elt.text
            #轉換變數名稱為全形
            var_name=ToFullWidthString(var_name)
            #獲取賦值內容
            value_elt=FindCurrent(block_elt,'value[name="VALUE"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            #輸出程式
            com_str+=f'{var_name} := {value_str}\n'

        elif block_elt.attrs['type']=="math_change":
            field_elt=FindCurrent(block_elt,'field[name="VAR"]')
            var_name=field_elt.text
            #轉換變數名稱為全形
            var_name=ToFullWidthString(var_name)
            value_str="0"
            #獲取賦值內容
            value_delta_elt=FindCurrent(block_elt,'value[name="DELTA"]')
            #若有放置數字blockly
            if FindCurrent(value_delta_elt,'block'):
                value_str,value_comment=AHK_value(value_delta_elt)
                com_str+=value_comment
            #若為預設影子blockly
            else:
                shadow_elt=FindCurrent(value_delta_elt,'shadow')
                value_str=FindCurrent(shadow_elt,'field').text
            
            #輸出程式
            com_str+=f'{var_name} += {value_str}\n'


        #endregion 變數Blockly

        #region 邏輯Blockly
        
        elif block_elt.attrs['type']=="controls_if":
            #獲取判斷布林值
            value_if0_elt=FindCurrent(block_elt,'value[name="IF0"]')
            value_if0_str,value_if0_comment=AHK_value(value_if0_elt,get_all_comment=True)
            com_str+=value_if0_comment
            #獲取執行式
            statement_do0_elt=FindCurrent(block_elt,'statement[name="DO0"]')
            statement_do0_str=AHK_statement(statement_do0_elt)
            com_str+=f"if {value_if0_str} {{\n{statement_do0_str}}}"

            mutation_elt=FindCurrent(block_elt,'mutation')
            #若是多層if層次block
            if mutation_elt:
                if mutation_elt.attrs.get('elseif'):
                    nb_elseif_int=int(mutation_elt.attrs.get('elseif'))
                    for i in range(1,nb_elseif_int+1):
                        #獲取判斷布林值
                        value_ifn_elt=FindCurrent(block_elt,f'value[name="IF{i}"]')
                        value_ifn_str,value_ifn_comment=AHK_value(value_ifn_elt,get_all_comment=True)
                        #取消註解的斷行，讓其出現在 }else if () { 同一行的後段
                        value_ifn_comment=value_ifn_comment.replace('\n','')
                        #獲取執行式
                        statement_don_elt=FindCurrent(block_elt,f'statement[name="DO{i}"]')
                        statement_don_str=AHK_statement(statement_don_elt)
                        
                        com_str+=f"else if {value_ifn_str} {{ {value_ifn_comment}\n{statement_don_str}}}"
                if mutation_elt.attrs.get('else'):
                    #獲取執行式
                    statement_doElse_elt=FindCurrent(block_elt,'statement[name="ELSE"]')
                    statement_doElse_str=AHK_statement(statement_doElse_elt)
                    com_str+=f"else {{\n{statement_doElse_str}}}"
            com_str+='\n'           

        #邏輯not
        elif block_elt.attrs['type']=="logic_negate":
            value_elt=FindCurrent(block_elt,'value[name="BOOL"]')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            com_str+=f'not {value_str}'

        #邏輯null
        elif block_elt.attrs['type']=="logic_null":
            com_str+='""'    

        #邏輯真假
        elif block_elt.attrs['type']=="logic_boolean":
            field_op_elt=FindCurrent(block_elt,'field[name="BOOL"]')
            com_str+=field_op_elt.text

        #邏輯比較
        elif block_elt.attrs['type']=="logic_compare":
            #獲取操作類型
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            op_str_dict={
                'EQ':'=',
                'NEQ':'!=',
                'LT':'<',
                'LTE':'<=',
                'GT':'>',
                'GTE':'>=',
            }
            field_op_str=op_str_dict[field_op_elt.text]
            #獲取比較值A
            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,value_a_comment=AHK_value(value_a_elt)
            com_str+=value_a_comment
            #獲取比較值B
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,value_b_comment=AHK_value(value_b_elt)
            com_str+=value_b_comment
            #輸出程式
            com_str+=f'({value_a_str} {field_op_str} {value_b_str})'

        #邏輯操作(AND OR)
        elif block_elt.attrs['type']=="logic_operation":
            #獲取操作類型
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            field_op_str=field_op_elt.text
            #獲取比較值A
            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,value_a_comment=AHK_value(value_a_elt)
            com_str+=value_a_comment
            #獲取比較值B
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,value_b_comment=AHK_value(value_b_elt)
            com_str+=value_b_comment
            #輸出程式
            com_str+=f'({value_a_str} {field_op_str} {value_b_str})'

        #包含文字
        elif block_elt.attrs['type']=="in_str":
            #獲取主要文字
            value_text_elt=FindCurrent(block_elt,'value[name="text"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt)
            com_str+=value_text_comment
            #獲取次要對比文字
            value_subtext_elt=FindCurrent(block_elt,'value[name="sub_text"]')
            value_subtext_str,value_subtext_comment=AHK_value(value_subtext_elt)
            com_str+=value_subtext_comment
            #獲取要使用的函式名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            func_str="not "*(field_elt.text=="not_contain")+"InStr"
            #輸出程式
            com_str+=f'{func_str}({value_text_str},{value_subtext_str})'

        #按鍵狀態
        elif block_elt.attrs['type']=="get_key_state":
            #獲取按鍵名稱
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #輸出程式
            com_str+=f'GetKeyState("{value_str}")'
            




        #endregion 邏輯Blockly


        #region 文字Blockly (其他)
        elif block_elt.attrs['type']=="break_line_chr":
            com_str+="\"`n\""

        #endregion 文字Blockly (其他)


        #region 右鍵清單Blockly
        elif block_elt.attrs['type']=="right_click_menu":
            #預設選單名稱紀錄串列
            item_name_with_sapce_str_list=[]

            MyMenu_str=f'MyMenu_{id(block_elt)}'
            menu_myMenu_add_str=""
            label_str=""
            #遍歷所有項目
            statement_elt=FindCurrent(block_elt,'statement')
            #設置項目計數器(防止重複Lable名稱)
            i_item=1
            block_item_elt_list=[]
            block_item_elt=FindCurrent(statement_elt,'block')
            if block_item_elt:
                block_item_elt_list.append(block_item_elt)
                while FindCurrent(block_item_elt,'next'):
                    next_elt=FindCurrent(block_item_elt,'next')
                    block_item_elt=FindCurrent(next_elt,'block')
                    block_item_elt_list.append(block_item_elt)
            
            for block_item_elt in block_item_elt_list:


                if block_item_elt.attrs['type']=="right_click_menu_item":
                    #獲取項目名稱
                    field_itemName_elt=FindCurrent(block_item_elt,'field[name="item_name"]')
                    item_name_raw_str=field_itemName_elt.text
                    #製作選單項目名稱:轉換變數名稱為全形(排除空白)
                    item_name_with_sapce_str=ToFullWidthString(item_name_raw_str,excluded_str_list=[' '])
                    item_name_without_sapce_str=ToFullWidthString(item_name_raw_str)
                    #若單項目名稱重複，就增加一個點(再重複就累加) #註:重複的選單名稱會使AHK失效
                    while item_name_with_sapce_str in item_name_with_sapce_str_list:
                        item_name_with_sapce_str=item_name_with_sapce_str + '.'
                    #紀錄選單名稱
                    item_name_with_sapce_str_list.append(item_name_with_sapce_str)
                    print(item_name_with_sapce_str_list)

                    menu_myMenu_add_str+=f"Menu,{MyMenu_str},Add,{item_name_with_sapce_str},{item_name_without_sapce_str}_{i_item}_{id(block_elt)}\n"
                    #獲取執行式
                    statement_do_elt=FindCurrent(block_item_elt,'statement[name="DO"]')
                    statement_do_str=AHK_statement(statement_do_elt)
                    label_str+=f"{item_name_without_sapce_str}_{i_item}_{id(block_elt)}:\n{statement_do_str}return\n"
                    #增加項目計數
                    i_item+=1
                elif block_item_elt.attrs['type']=="right_click_menu_item_hr":
                    menu_myMenu_add_str+=f"Menu,{MyMenu_str},Add,\n"



            #輸出程式碼
            com_str+='''Loop,1{
CoordMode, Menu, Screen
CoordMode, Mouse, Screen

'''+ menu_myMenu_add_str +'''
MouseGetPos,MX,MY
Menu,'''+MyMenu_str+''',Show,% MX,% MY
Menu,'''+MyMenu_str+''',DeleteAll
return

'''+ label_str +'''}\n'''



        #endregion 右鍵清單

        #region 音量控制

        elif block_elt.attrs['type']=="volume_adjust":
            #獲取同整動作
            field_action_elt=FindCurrent(block_elt,'field[name="action"]')
            field_action_str=field_action_elt.text
            add_or_sub_symbol_str='+' if field_action_str=="add" else '-' if field_action_str=="sub" else ""
            #獲取調整數值
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else 0
            com_str+=value_comment
            #輸出程式碼
            com_str+=f"SoundSet {add_or_sub_symbol_str}{value_str}\n"

        elif block_elt.attrs['type']=="volume_mute":
            #輸出程式碼
            com_str+="SoundSet,+1, , mute\n"

        #endregion 音量控制

        #region 選取文字後
        elif block_elt.attrs['type']=="open_select_url":
            com_str+='\n'.join([
                'clipboard_save:=clipboard',
                'clipboard:=""',
                'Send ^{c}',
                'ClipWait',
                'Sleep 100',
                'Run %clipboard%',
                'clipboard:=clipboard_save\n'
            ])
       
        #選取文字進行關鍵字搜尋
        elif block_elt.attrs['type']=="search_selected_keyword":
            #獲取網站名稱元素
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            #網站名稱和對應的網址tuple字典
            search_selected_keyword_url_tuple_dict={
                'google':("https://www.google.com.tw/search?q=","","Google搜尋"),
                'youtube':("https://www.youtube.com/results?search_query=","","Youtube搜尋"),
                'baidu':("https://www.baidu.com/s?wd=","","百度搜尋"),
                'wiki':("http://zh.wikipedia.org/w/index.php?title=Special:Search&search=","","WIKI搜尋"),
                'google_map':("https://www.google.com.tw/maps/search/","","Google地圖搜尋"),
                'google_trend':("https://www.google.com/trends/explore?q=","","Google搜尋趨勢"),
                'google_translate':("https://translate.google.com.tw/?tab=wT#view=home&op=translate&sl=auto&tl=zh-TW&text=","","Gooogle翻譯"),
                'evernote':("https://www.evernote.com/client/web#?query=","","Evernote搜尋"),
                'facebook':("https://www.facebook.com/search/top/?q=","","Facebook搜尋"),
                'cdict':("https://cdict.net/?q=","","cdict(英翻中/中翻英)"),
                'plurk':("https://www.plurk.com/w/#","?time=365","噗浪搜尋"),
                'twitter':("https://twitter.com/search?q=","","推特搜尋"),
                'moedict':("https://www.moedict.tw/","","萌典(中文字典)"),
            }
            #獲取對應的網址
            search_selected_keyword_url_tuple=search_selected_keyword_url_tuple_dict[field_elt.text]
            urlA_str, urlB_str, website_name=search_selected_keyword_url_tuple
            com_str+='\n'.join([
                f'__UrlA:="{urlA_str}"',
                f'__UrlB:="{urlB_str}"',
                f'__WebsiteName:="{website_name}"',
                'clipboard_save:= clipboard',
                'clipboard:=""',
                'Send ^{c}',
                'Sleep 100',
                '__keyWord:= clipboard',
                'Clipboard = %clipboard_save%',
                'if not __keyWord {',
                '    if not __WebsiteName{',
                '        __WebsiteName:=__UrlA',
                '    }',
                '    InputBox, __keyWord,搜尋關鍵字,%__WebsiteName%,,,150',
                '}',
                'if (ErrorLevel=0 and __keyWord!=""){',
                '    VarSetCapacity(__Var, StrPut(__keyWord, "UTF-8"), 0)',
                '    StrPut(__keyWord, &__Var, "UTF-8")',
                '    f := A_FormatInteger',
                '    SetFormat, IntegerFast, H',
                '    While __Code := NumGet(__Var, A_Index - 1, "UChar")',
                '        If (__Code >= 0x30 && __Code <= 0x39 ; 0-9',
                '            || __Code >= 0x41 && __Code <= 0x5A ; A-Z',
                '            || __Code >= 0x61 && __Code <= 0x7A) ; a-z',
                '            __Res .= Chr(__Code)',
                '        Else',
                '            __Res .= "%" . SubStr(__Code + 0x100, -1)',
                '    SetFormat, IntegerFast, %f%',
                '    Run %__UrlA%%__Res%%__UrlB%',
                '    __Res:=""',
                '    __Var:=""',
                '}',
                '_keyWord:=""\n',
            ])

        #選取文字進行關鍵字搜尋
        elif block_elt.attrs['type']=="search_selected_keyword_custom":
            #獲取網站名稱元素
            field_websiteName_elt=FindCurrent(block_elt,'field[name="website_name"]')
            website_name=field_websiteName_elt.text
            field_urlA_elt=FindCurrent(block_elt,'field[name="url_a"]')
            urlA_str=field_urlA_elt.text
            field_urlB_elt=FindCurrent(block_elt,'field[name="url_b"]')
            urlB_str=field_urlB_elt.text
            com_str+='\n'.join([
                f'__UrlA:="{urlA_str}"',
                f'__UrlB:="{urlB_str}"',
                f'__WebsiteName:="{website_name}"',
                'clipboard_save:= clipboard',
                'clipboard:=""',
                'Send ^{c}',
                'Sleep 100',
                '__keyWord:= clipboard',
                'Clipboard = %clipboard_save%',
                'if not __keyWord {',
                '    if not __WebsiteName{',
                '        __WebsiteName:=__UrlA',
                '    }',
                '    InputBox, __keyWord,搜尋關鍵字,%__WebsiteName%,,,150',
                '}',
                'if (ErrorLevel=0 and __keyWord!=""){',
                '    VarSetCapacity(__Var, StrPut(__keyWord, "UTF-8"), 0)',
                '    StrPut(__keyWord, &__Var, "UTF-8")',
                '    f := A_FormatInteger',
                '    SetFormat, IntegerFast, H',
                '    While __Code := NumGet(__Var, A_Index - 1, "UChar")',
                '        If (__Code >= 0x30 && __Code <= 0x39 ; 0-9',
                '            || __Code >= 0x41 && __Code <= 0x5A ; A-Z',
                '            || __Code >= 0x61 && __Code <= 0x7A) ; a-z',
                '            __Res .= Chr(__Code)',
                '        Else',
                '            __Res .= "%" . SubStr(__Code + 0x100, -1)',
                '    SetFormat, IntegerFast, %f%',
                '    Run %__UrlA%%__Res%%__UrlB%',
                '    __Res:=""',
                '    __Var:=""',
                '}',
                '_keyWord:=""\n',
            ])
       

        #endregion 選取文字後



        #region 系統資訊Blockly

        elif block_elt.attrs['type']=="system_info_str":
            #獲取選取名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            #若選擇本用戶名稱
            if field_elt.text=="user_name":
                com_str+="A_UserName"
            elif field_elt.text=="computer_name":
                com_str+="A_ComputerName"

        elif block_elt.attrs['type']=="system_info_num":
            #獲取選取名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            #若選擇本用戶名稱
            if field_elt.text=="screen_width":
                com_str+="VirtualWidth"
                func_dict_key_set.update(['screen_width'])
            elif field_elt.text=="screen_height":
                com_str+="VirtualHeight"
                func_dict_key_set.update(['screen_height'])


        elif block_elt.attrs['type']=="computer_name":
            com_str+="A_ComputerName"

        elif block_elt.attrs['type']=="user_name":
            com_str+="A_UserName"

        elif block_elt.attrs['type']=="win_get_active_title":
            #獲取變數名稱
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment

            com_str+=f'WinGetActiveTitle, {value_str}\n'

        #endregion 系統資訊Blockly

        #region 循環Blockly

        #Loop循環
        elif block_elt.attrs['type']=="controls_repeat_ext":
            #獲取重複次數
            value_elt=FindCurrent(block_elt,'value[name="TIMES"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            loop_time_int_var_name=f'loop_time_int_{id(block_elt)}'
            com_str+=f"{loop_time_int_var_name}:={value_str}\n"
            com_str+=f"Loop %{loop_time_int_var_name}% {{\n{statement_do_str}}}\n"

        #For Loop 循環
        elif block_elt.attrs['type']=="controls_for":
            #獲取開始數
            value_from_elt=FindCurrent(block_elt,'value[name="FROM"]')
            value_from_str,value_from_comment=AHK_value(value_from_elt,get_all_comment=True)
            com_str+=value_from_comment
            #獲取中止數
            value_to_elt=FindCurrent(block_elt,'value[name="TO"]')
            value_to_str,value_to_comment=AHK_value(value_to_elt,get_all_comment=True)
            com_str+=value_to_comment
            #獲取間隔數
            value_by_elt=FindCurrent(block_elt,'value[name="BY"]')
            value_by_str,value_by_comment=AHK_value(value_by_elt,get_all_comment=True)
            com_str+=value_by_comment
            #獲取變數名稱
            field_var_elt=FindCurrent(block_elt,'field[name="VAR"]')
            field_var_str=field_var_elt.text
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            #輸出程式碼
            start_var_str=f"_start_{id(block_elt)}"
            end_var_str=f"_end_{id(block_elt)}"
            step_var_str=f"_step_{id(block_elt)}"
            looptime_var_str=f"_looptime_{id(block_elt)}"
            com_str+='\n'.join([
                f"{start_var_str}:={value_from_str}",
                f"{end_var_str}:={value_to_str}",
                f"{step_var_str}:=({end_var_str}>{start_var_str})?Abs({value_by_str}):-Abs({value_by_str})",
                f"{looptime_var_str}:=(Abs({start_var_str}-{end_var_str})//Abs({step_var_str}))+1",
                f"Loop % {looptime_var_str} {{",
                f"{TAB_SPACE}{field_var_str}:={start_var_str}+(A_index-1)*{step_var_str}",
                f"{statement_do_str}}}\n"
            ])

            #com_str+=f"Loop {value_str} {{\n{statement_do_str}}}\n"

        #while循環
        elif block_elt.attrs['type']=="controls_whileUntil":
            #獲取布林值
            value_elt=FindCurrent(block_elt,'value[name="BOOL"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "False"
            com_str+=value_comment
            #獲取迴圈方式
            field_elt=FindCurrent(block_elt,'field[name="MODE"]')
            while_str="while"+" not"*(field_elt.text!="WHILE")
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            com_str+=f"{while_str} {value_str} {{\n{statement_do_str}}}\n"

        #break或continue
        elif block_elt.attrs['type']=="controls_flow_statements":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=field_elt.text.lower()+'\n'

        #while true
        elif block_elt.attrs['type']=="while_true":
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            com_str+=f"while TRUE {{\n{statement_do_str}}}\n"

        elif block_elt.attrs['type']=="controls_forEach":
            #獲取循環用的變量名稱
            field_var_elt=FindCurrent(block_elt,'field[name="VAR"]')
            field_var_str=field_var_elt.text
            #獲取串列物件
            value_elt=FindCurrent(block_elt,'value[name="LIST"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "Array()" #若沒有放入串列積木，則預設為空字串
            com_str+=value_comment       
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            #輸出程式碼
            com_str+=f'For _,{field_var_str} in {value_str} {{\n{statement_do_str}}}\n'

        

        #endregion 循環Blockly

        #串列
        elif block_elt.attrs['type']=="lists_create_with":
            #獲取串列長度
            mutation_elt=FindCurrent(block_elt,'mutation')
            mutation_items_int=int(mutation_elt.attrs['items'])
            value_str_list=[]
            #
            for i_item in range(mutation_items_int):
                value_elt=FindCurrent(block_elt,f'value[name="ADD{i_item}"]')
                value_str,value_comment=AHK_value(value_elt)
                value_str_list.append(value_str)
            #輸出程式碼
            com_str+=f'Array({", ".join(value_str_list)})'

        #字串化串列
        elif block_elt.attrs['type']=="list_str":
            #註冊關聯函數
            func_dict_key_set.update(['ArrayStr'])
            #獲取串列物件
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "Array()" #若沒有放入串列積木，則預設為空字串
            com_str+=f'ArrayStr({value_str})'
            


        #region 自訂程式碼Blockly

        elif block_elt.attrs['type']=="ahk_code":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=field_elt.text+'\n'

        elif block_elt.attrs['type']=="cmd":
            #獲取CMD程式碼
            field_code_elt=FindCurrent(block_elt,'field[name="code"]')
            cmd_code_str=field_code_elt.text
            #獲取使否執行後關閉
            field_doClose_elt=FindCurrent(block_elt,'field[name="do_close"]')
            arg_str='/c' if field_doClose_elt.text=="TRUE" else '/k'

            com_str+=f'Run %comspec% {arg_str} {cmd_code_str}\n'

        #endregion 自訂程式碼Blockly

        #region 螢幕

        #亮度控制
        elif block_elt.attrs['type']=="set_brightness":
            #註冊關聯函數
            func_dict_key_set.update(['SetBrightness'])
            #獲取同整動作
            field_action_elt=FindCurrent(block_elt,'field[name="action"]')
            field_action_str=field_action_elt.text
            add_or_sub_symbol_str='+' if field_action_str=="add" else '-' if field_action_str=="sub" else ""
            #獲取調整數值
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else 0
            com_str+=value_comment
            #輸出程式碼
            com_str+='\n'.join([
                'global __vBright',
                f'__vBright{add_or_sub_symbol_str}={value_str}',
                '__vBright:=Max(Min(100,__vBright),0)',
                'SetBrightness(__vBright)\n',
            ])

        #關閉顯示器
        elif block_elt.attrs['type']=="close_monitor":
            #輸出程式碼
            com_str+='\n'.join([
                "Sleep 1000 ; 設定一秒延遲以防釋放按鍵時會喚醒螢幕",
                "SendMessage 0x112, 0xF170, 2,,Program Manager ; send the monitor into standby (off) mode\n"
            ])

        elif block_elt.attrs['type']=="screenshot":
            #增加關聯函數鍵值集合
            func_dict_key_set.update(['FullwidthSymbol','Screenshot'])
            #獲取檔案路徑
            value_path_elt=FindCurrent(block_elt,'value[name="path"]')
            value_path_str,value_path_comment=AHK_value(value_path_elt,get_all_comment=True)
            value_path_str=value_path_str if value_path_str else ""
            com_str+=value_path_comment
            #獲取圖片檔名稱
            value_filename_elt=FindCurrent(block_elt,'value[name="filename"]')
            value_filename_str,value_filename_comment=AHK_value(value_filename_elt,get_all_comment=True)
            value_filename_str=value_filename_str if value_filename_str else ""
            com_str+=value_filename_comment
            #獲取圖片附檔名名稱
            field_subfilename_elt=FindCurrent(block_elt,'field[name="subfilename"]')
            field_subfilename_str=field_subfilename_elt.text if field_subfilename_elt.text in ['.png','.jpg'] else ""
            #輸出程式碼
            com_str+='\n'.join([
                f'_fullfilename := {value_path_str} . "/" .  FullwidthSymbol({value_filename_str}) . "{field_subfilename_str}"',
                f'Screenshot(_fullfilename)\n',
            ])


        #endregion 螢幕亮度控制

        #處理下一個block
        next_elt=FindCurrent(block_elt,'next',get_one=True)
        if next_elt:
            block_next_elt=FindCurrent(next_elt,'block')
            com_str+=AHK_block(block_next_elt)

    if separate_comment:
        return  com_str,comment_str   
    else:
        return comment_str+com_str



#綁定事件:workspace更換時就轉譯blocks為xml
def ClearAhkCodeArea(ev):
    #清空AHK code
    doc['textarea_ahk'].innerHTML=""
    #禁用複製和下載AHK檔案按鈕
    for btn_elt in doc['div_copy_ahkfile_btns_area'].select('button'):
        btn_elt.disabled=True
        btn_elt.classList.add('disabled_button')


workspace.addChangeListener(ClearAhkCodeArea)

#綁定事件:停用落單的blockly
#workspace.addChangeListener(Blockly.Events.disableOrphans);


#定義匯入積木檔 XML 的動作
def ImportXmlCode(ev):    
    #定義匯入XML積木檔案時的解析動作
    def OnInputXmlFile(ev):
        #定義文字讀取完後的動作
        def ReaderOnload(ev):
            #獲取積木檔 XML 內容
            xml_code=ev.target.result
            #覆蓋到積木 XML 文字區域
            doc['textarea_xml'].value = xml_code
            #觸發 XML 渲染事件
            XmlToBlockly(window.Event.new("input"))
        
        #獲取 XML 檔案
        inputFileElt=ev.target
        inputFile=inputFileElt.files[0]
        #建立檔案讀取DOM實例，並解析XML積木檔內容文字
        reader = window.FileReader.new()
        reader.readAsText(inputFile)
        reader.bind("load", ReaderOnload)


    #創造一個開啟檔案的 input 元素並進行點擊，觸發解析動作函數
    inputFileElt=INPUT(type='file',accept='text/xml') #限制開啟檔案類型為 XML 檔案
    inputFileElt.bind('input',OnInputXmlFile)
    inputFileElt.click()

#定義動作:下載XML積木檔案
def DownloadXmlCode(ev):
    #先點擊 [轉換為AHK語法] 按鈕，確保AHK轉譯至XML完畢
    doc['btn_blockToAhk'].click()
    #獲取積木 XML 結構並輸出 XML 檔案
    xml_code=doc['textarea_xml'].value
    filename="myahkblockly.xml"
    DownloadTextFile(filename,xml_code)

#設置AHK語法轉換結果畫面元素
div_showAhkArea_elt=DIV(id="div_show_ahk_area")

#設置橫幅DIV元素，並填充文字和複製、下載按鈕
div_showAhkAreaHeader_elt=DIV(id="div_show_ahk_btns")
div_showAhkAreaHeader_elt<=BUTTON("▼轉換為AHK語法",id="btn_blockToAhk").bind("click",BlocklyToXml)
div_showAhkAreaHeader_elt<=BUTTON("💾另存積木檔").bind("click",DownloadXmlCode)
div_showAhkAreaHeader_elt<=BUTTON("📥匯入積木檔").bind("click",ImportXmlCode)

#定義動作:複製AHK語法
def CopyAhkCode(ev):
    ahk_code=doc['textarea_ahk'].innerHTML
    CopyTextToClipborad(ahk_code)
    alert('複製成功!')

#定義動作:下載AHK檔案
def DownloadAhkCode(ev):
    ahk_code=JavascriptSymbolDecoder(doc['textarea_ahk'].innerHTML)
    filename="myahk.ahk"
    DownloadTextFile(filename,ahk_code)

countdown_timer=None
sec_int=None
#定義動作:轉譯成AHK.exe檔並下載
def DownloadAhkExe(ev):
    global countdown_timer,sec_int
    #host="http://127.0.0.1:8001"
    ##!!
    host="https://e60809097704.ngrok.io"
    btn_elt=ev.currentTarget

    #停用按鍵
    btn_elt.disabled=True
    btn_elt.classList.add('disabled_button')
    
    sec_int=10
    #定義動作:在按鈕文字上顯示等待時間
    def waitting_compile_countdown():
        global sec_int
        btn_elt.text=f"轉譯中...(約{sec_int}秒等待)"
        sec_int=sec_int-1 if sec_int!=0 else 0

    btn_text=btn_elt.text
    countdown_timer=timer.set_interval(waitting_compile_countdown,1000)
    
    #定義完成送出AHK程式碼後的動作
    def on_complete(res):
        #停止倒數
        global countdown_timer
        timer.clear_interval(countdown_timer)
        countdown_timer=None
        #獲取檔名key
        filename_key=res.text
        window.open(f"{host}/dl?filename_key={filename_key}","_parent")
        #恢復按鍵文字訊息
        btn_elt.text="下載中..."

        #定義刪除檔案動作
        def rm_ahk_exe():
            req = ajax.ajax()
            url=f"{host}/rm?filename_key={filename_key}"
            req.open('GET',url,True)
            req.set_header('content-type','application/x-www-form-urlencoded')
            req.send()
            btn_elt.text=btn_text
            #啟用按鍵
            btn_elt.disabled=False
            btn_elt.classList.remove('disabled_button')


        #數秒後送出刪除檔案請求
        timer.set_timeout(rm_ahk_exe,10000)

    #獲取AHK程式碼
    ahk_code=doc['textarea_ahk'].innerHTML
    #轉換JS字元，如 &amp; -> &
    ahk_code=JavascriptSymbolDecoder(ahk_code)
    #獲取作業系統類型(64/32位元)
    btn_elt=ev.currentTarget
    os_type_str=';__32-bit__;\n' if btn_elt.id=="btn_dl32exe" else ';__64-bit__;\n'
    #送出post請求
    req = ajax.ajax()
    req.bind('complete',on_complete)
    url=f"{host}/cp"
    req.open('POST',url,True)
    req.set_header('content-type','application/x-www-form-urlencoded')
    req.send(os_type_str+ahk_code)

#設置複製和下載按鈕
div_showAhkAreaBtns_elt=DIV(id="div_copy_ahkfile_btns_area")
div_showAhkAreaBtns_elt<=BUTTON("複製語法").bind("click",CopyAhkCode)
div_showAhkAreaBtns_elt<=BUTTON("下載.ahk檔案").bind("click",DownloadAhkCode)
div_showAhkAreaBtns_elt<=BUTTON("下載.exe檔(64-bit)",style={'color':'#000094'},id="btn_dl64exe").bind("click",DownloadAhkExe)

div_showAhkAreaBtns_elt<=SPAN("←測試功能 (")+A("檢測到病毒?有何風險?",href="https://hackmd.io/hcAlG6oeQNO1jpILguR5hw?view")+SPAN(")")

#排版
div_showAhkArea_elt<=div_showAhkAreaHeader_elt
div_showAhkArea_elt<=PRE(
    id="textarea_ahk",
)
div_showAhkArea_elt<=div_showAhkAreaBtns_elt


#設置XML轉換結果畫面元素
div_textareaXml_elt=DIV(id='input_xml_area')
#實際部屬時，要把XML區塊隱藏起來
if 'herokuapp' in window.location.hostname:
    div_textareaXml_elt.style.display="none"
div_textareaXml_elt
div_textareaXml_elt<=P("xml:")
textarea_showXml_elt=TEXTAREA(
    id="textarea_xml",
)
textarea_showXml_elt.bind('input',XmlToAHK)
textarea_showXml_elt.bind('input',XmlToBlockly)
div_textareaXml_elt<=textarea_showXml_elt


#設置使用說明iframe
iframe_elt=IFRAME(src="https://hackmd.io/@papple23g/r1RuM08tB")
div_iframe_elt=DIV(iframe_elt)

#設置子頁面標頭DIV元素
div_title_elt=DIV()
#設置標頭H1元素
VERSION="1.12.0" ###
h1_title_elt=H1(f"AutoHotKey 積木語法產生器 v{VERSION}",style={"color":"rgb(220, 107, 57)","font-size":"18px","font-weight":"600",'float':'left'})
#設置FB DIV元素
div_fb_elt=DIV(id='div_fb',style={'float':'right'})
div_fb_elt.innerHTML=r'<div id="fb-root" style="float:right"></div><div class="fb-like" data-href"https://papple23g-ahkcompiler.herokuapp.com/ahkblockly" data-layout="button_count" data-action="like" data-size="small" data-show-faces="false" data-share="true"></div>' # style="float:right"
#
div_title_elt<=h1_title_elt
div_title_elt<=div_fb_elt+DIV(style={'clear':'both'})

#排版

#設置版本標題
doc['div_ahkblockly_gui'].insertBefore(div_title_elt,doc['div_ahkblockly_gui'].select_one('div'))
#載入完Brython後才顯示workspace區塊 (才能一併顯示頁面)
doc['blocklyDiv'].style.visibility="visible"
#在ahkblockly_gui置入程式碼區塊
doc['div_ahkblockly_gui']<=div_showAhkArea_elt
doc['div_ahkblockly_gui']<=div_textareaXml_elt
#置入說明區塊
doc['div_subMainPage']<=div_iframe_elt
AddStyle('''

    #div_ahkblockly_gui {
        width: 69% !important;
        float: left;
        margin-bottom: 150px;

    }

    iframe{
        float: left;
        border: none;
        width: 30%;
        min-width: 200px;
        height: 1000px;
    }

    @media only screen and (max-width: 911px) {
        #div_ahkblockly_gui {
            width: 90% !important;
        }
        iframe{
            width: 90%;
        }
    }

    #div_copy_ahkfile_btns_area a {
        color:#0505b3 !important;
    }

    #div_copy_ahkfile_btns_area a:hover {
        color:#4a7aff !important;
    }

    .blocklyText, .blocklyHtmlInput, .blocklyTreeLabel {
        font-family: '微軟正黑體', sans-serif !important;
        font-weight: 600;
    }
''')
#調整workspace為符合當前頁面的尺寸
Blockly.svgResize(workspace)

#定義動作:儲存
def StoringXml(ev):
    #獲取workspace blockly的xml
    xml_str=Blockly.Xml.workspaceToDom(workspace).outerHTML
    #紀錄xml到暫存空間
    storage['xml']=xml_str
workspace.addChangeListener(StoringXml)


#首次載入網頁時，若暫存空間裡有xml的資料，就印出該資資料
if 'xml' in storage.keys():
    #獲取之前儲存的xml資料
    doc['textarea_xml'].value=storage['xml']
    #觸發xml轉Blockly
    doc['textarea_xml'].dispatchEvent(window.Event.new("input"))
#否則，解析workspace
else:
    BlocklyToXml(window.Event.new("change"))



#{% endverbatim %}