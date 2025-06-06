TITLE Low-level I/O Procedures and Implementing Macros

; Author:			Duane Goodner
; Contact info:	dmgoodner@gmail.com
; Description:			Gets 10 integer values from user entered as strings. Converts string values
;				to numeric integer values, and stores these values in an array. Converts
;				integers back to strings and outputs the list of values to screen. Computes
;				sum of the integers, and outputs this value to screen as a string. Then computes
;				mean of the list of integers (rounded down using floor division) and prints
;				this value to screen as as a string.


include Irvine32.inc
include Macros.inc
includelib Kernel32.lib
includelib Irvine32.Lib
includelib User32.lib


MAX_INP_LEN = 30					; Max length of input string
NUM_INT = 10						; Number of integers to get from user
MAX_OUT_LEN = 12					; Max length of output string ('-' + 10 digits + terminating 0)

getString MACRO prompt_address, instring_address
	push     ecx
	push     edx
	mov      edx, prompt_address
	call     WriteString
	mov      edx, instring_address
	mov      ecx, MAX_INP_LEN - 1
	call     ReadString
	pop      edx
	pop      ecx
ENDM

displayString MACRO string_offset
	push	 edx
	mov	 edx, string_offset
	call	 WriteString
	pop	 edx
ENDM

dislplayCharacter MACRO character
	push	 eax
	mov	 al, character
	call	 WriteChar
	pop	 eax
ENDM


.data

intro_1      BYTE	"Low-level I/O Procedures and Implementing Macros", 10, 13, 0
intro_2      BYTE	"Computer Architecture & Assembly Language Portfolio Project, March 2020", 10, 13, 0
desc_1       BYTE	"Please provide 10 signed decimal integers.", 10, 13, 0
desc_2       BYTE	"Each number needs to be small enough to fit inside a 32 bit register.", 10, 13, 0
desc_3       BYTE	"After you have finished inputting the raw numbers a list of the integers,", 10, 13, 0
desc_4       BYTE	"their sum, and their average value will be displayed.", 10, 13, 0
entry_req    BYTE 	"Please enter a signed integer: ", 0
error_msg    BYTE	"ERROR: You did not enter a signed number or your number was too big.", 10, 13, 0
list_title   BYTE	"You entered the following numbers:", 10, 13, 0
sum_title    BYTE	"The sum of these numbers is: ", 0
mean_title   BYTE	"The rounded average (determined using floor division) is: ", 0
byebye       BYTE	"Goodbye, and thanks for playing!", 0

input_str    BYTE	MAX_INP_LEN DUP (?)
output_str   BYTE	MAX_OUT_LEN DUP (?)

int_array    SDWORD	NUM_INT DUP (?)
array_sum    SDWORD	?
array_mean   SDWORD	?



.code
main PROC

; Introduce program
	push     OFFSET intro_1
	push     OFFSET intro_2
	push     OFFSET desc_1
	push     OFFSET desc_2
	push     OFFSET desc_3
	push     OFFSET desc_4
	call     introduction


; Get user values (and validate and convert str to numeric)
	push     OFFSET entry_req
	push     OFFSET error_msg
	push     OFFSET input_str
	push     OFFSET int_array
	call     getUserIntegers


; Display array with list of integers
	push     OFFSET list_title
	push     OFFSET int_array
	push     LENGTHOF int_array
	push     TYPE int_array
	push     OFFSET output_str
	call     displayList


; Compute sum and average
	push     OFFSET int_array
	push     LENGTHOF int_array
	push     OFFSET array_sum
	push     OFFSET array_mean
	call     computeSumAndMean


; Display sum
	push     OFFSET sum_title
	push     OFFSET array_sum
	push     OFFSET LENGTHOF array_sum
	push     TYPE array_sum
	push     OFFSET output_str
	call     displayList


; Display average
	push     OFFSET mean_title
	push     OFFSET	array_mean
	push     OFFSET LENGTHOF array_mean
	push     TYPE array_mean
	push     OFFSET output_str
	call     displayList


; Say goodbye
	push     OFFSET byebye
	call     farewell


	exit	; exit to operating system
main ENDP


;-----------------------------------------------------------------------------------
; introduction
; Introduces and describes program
;
; Receives: 		intro1_address, intro2_address, desc1_address, desc2_address,
; 			desc3_address, desc4_address (addresses of strings for intro 
;			and instructions)
;
; Returns:		None
;
; Preconditions:	Immediately prior to calling, main pushes arguments to stack
;                       in the following order: intro1_address, intro2_address
;			desc1_address, desc2_address, desc3_address, desc4_address
;
; Post-conditions:	Nothing changed in memory (but introduction message and 
;			program description displayed to screen)
;
; Registers Changed:	None
;-----------------------------------------------------------------------------------

introduction PROC USES edx,
	desc4_address:PTR DWORD,
	desc3_address:PTR DWORD,
	desc2_address:PTR DWORD,
	desc1_address:PTR DWORD,
	intro2_address:PTR DWORD,
	intro1_address:PTR DWORD

; Use macro to display strings to screen
	displayString intro1_address
	call 	 CrLF
	displayString intro2_address
	call	 CrLf
	call	 CrLf
	displayString desc1_address
	displayString desc2_address
	displayString desc3_address
	displayString desc4_address
	call	 CrLf

	ret
introduction ENDP


;-----------------------------------------------------------------------------------
; get_user_integers
; Builds array containing list of 10 integers input by user. Each integer is
; obtained by calling readVal which gets user's string of digits and converts
; that string to a numeric value.
;
; Receives:			entry_req_address = address of string requesting data
;				error_msg_address = error message strings address
;				input_str_address = Address of array that will store user string
;				int_array_address = address of array that will store numeric values
;
; Returns:			User integers stored in int_array.
;
; Preconditions:		Calling procedure pushes parameters to stack in
;				following order: 
;				entry_req_address, error_msg_address, input_str_address,
;				int_array_address
;
; Post-conditions:		User integers stored as numeric values in int_array. String
;				entered during final call of readVal will remain in input_str.
;
; Registers Changed:	None
;-----------------------------------------------------------------------------------

getUserIntegers PROC USES eax ecx edi,
	int_array_address:PTR DWORD,
	input_str_address:PTR DWORD,
	error_msg_address:PTR DWORD,
	entry_req_address:PTR DWORD
	LOCAL list_length:DWORD

	mov      list_length, NUM_INT
	mov      ecx, list_length			; set counter
	mov      edi, int_array_address			; move edi to 1st element of storage array
	cld						; direction = forward

; Call readVal procedure to run ascii to integer conversion algorithm
get_next_entry:
	push     entry_req_address
	push     error_msg_address
	push     input_str_address
	push     edi
	call     readVal

	add	 edi, 4					; advance edi to next element of write array

	loop	 get_next_entry				; loop to next call of readVal
	call	 CrLf

	ret
getUserIntegers ENDP


;-----------------------------------------------------------------------------------
; readVal
; Gets user data as a string. Calls other procedures to convert to signed integer,
; validate data, and store integer in array.
;
; Receives:			entry_req_address = address of string requesting data
;				error_msg_address = error message strings address
;				input_str_address = Address of array that will store user string
;				array_element_address = address where converted integer gets stored
;
; Returns:			Numeric value stored at location specified by
;				array_element_address
;
; Preconditions:		Calling procedure pushes parameters to stack in
;				following order: 
;				entry_req_address, error_message_address,
;				input_str_address, array_element_address.
;
; Post-conditions:		Numeric value of string stored at locaton specified by
;				array_element_address. String from last call remains at
;				location specified by input_str_address.
;
; Registers Changed:		None
;-----------------------------------------------------------------------------------

readVal PROC USES eax ebx ecx edx esi edi,
	array_element_address:PTR DWORD,
	input_str_address:PTR DWORD,
	error_msg_address:PTR DWORD,
	entry_req_address:PTR DWORD
	LOCAL length_of_string:DWORD,
	sign_one:SDWORD

; Use macro to get and store user string
get_input:
	getString entry_req_address, input_str_address

	mov      edi, array_element_address

	mov      length_of_string, eax
	mov      ecx, eax				; set loop counter to length of string
	mov      esi, input_str_address

; Check for + and - sign at first element
	mov      sign_one, 1				; will change to -1 if 1st char is '-'
	mov      al, [esi]
	cmp      al, 43					; check if 1st char is '+'
	jne      check_for_minus_sign
	inc      esi					; if 1st char is '+' advance esi 1 Byte...
	dec      ecx					; and reduce counter by 1
check_for_minus_sign:
	mov      al, [esi]
	cmp      al, 45
	jne      check_for_numeric
	mov      sign_one, -1
	inc      esi
	dec      ecx

check_for_numeric:
	mov      eax, 0					; initialize eax before using lodsb
	mov      ebx, 0
	cld

conversion_algorithm:
	lodsb						; load ascii val of next byte

	; check if ascii val --> 0 - 9
	cmp      al, 48
	jl       invalid_data
	cmp      al, 57
	jg       invalid_data

	sub      al, 48					; convert numeric ascii value to corresponding numeric

	movzx    edx, al				; put in 32 bit reg to be safe. Sign extending may also be OK?
	imul     edx, sign_one				; if value is neg, this changes edx to neg

	imul     ebx, 10				; multiply by 10 for each digit
	jo       invalid_data				; check for overflow
	add      ebx, edx				; add current loop's digit (*10^0 = 1)
	jo       invalid_data				; check for overflow

	loop     conversion_algorithm

	jmp      valid_entry

invalid_data:
	displayString error_msg_address
	jmp      get_input

valid_entry:
	mov      [edi], ebx

	ret
readVal ENDP

;-----------------------------------------------------------------------------------
; displayList
; Displays elements of an array of numeric values. Calls writeVal to convert each
; numeric value to a character string.
;
; Receives:			output_str_address = address of string array used to write
;				converted data before it is displayed
;				element_size = size of array elements used to store numeric value
;				list_length = number of elements in array of values
;				array_address = address of array where numeric values are stored
;				list_title_address = address of string with list title/desc
;
; Returns:			None.
;
; Preconditions:		Calling procedure must push parameters to stack in following
;				order: list_title_address, array_address, element_size,
;				output_str_address
;
; Post-conditions:		String displayed to screen, and sring from last call of
;				writeVal remains at memory location specified by
;				output_str_address.
;
; Registers Changed:		None
;-----------------------------------------------------------------------------------

displayList PROC USES ecx esi edi,
	output_str_address:PTR DWORD,
	element_size:DWORD,
	list_length:DWORD,
	array_address:PTR DWORD,
	list_title_address:PTR DWORD

	mov      ecx, list_length			; initialize loop counter
	mov      esi, array_address			; set esi to address of 1st list element
	mov      edi, output_str_address		; edi points to desination string

	displayString list_title_address		; use macro

; Call writeVal procedure to write each element
write_list_elements:
	push     edi
	push     esi
	call     writeVal
	add      esi, element_size			; advance to next element of array
	cmp      ecx, 1
	je       after_comma_space

	dislplayCharacter ','				; if not at last element, need ', '
	dislplayCharacter ' '

after_comma_space:

	loop     write_list_elements
	call     CrLf
	call     CrLf

	ret
displayList ENDP



;-----------------------------------------------------------------------------------
; writeVal
; Converts a numeric value into a string of digits that represent that value in
; decimal form, and outputs this string to the terminal.
;
; Receives:			integer_address = address of integer to conver to string
;				string_address = address where converted string is stored
;
; Returns:			None.
;
; Preconditions:		Calling procedure must push in following order:
;				string_address, nteger_address
;
; Post-conditions:		Converted string displayed to screen. String from latest call
;				will remain at string_address.
;
; Registers Changed:		None
;-----------------------------------------------------------------------------------

writeVal PROC USES esi edi ecx eax ebx edx,
	integer_address:PTR DWORD,
	string_address:PTR DWORD
	LOCAL int_value:SDWORD,
	sign_one:SDWORD

	mov      edi, string_address			; point edi to output string
	mov      ecx, MAX_OUT_LEN			; initialize counter
	mov      al, 0
	cld						; direction = forward
	rep      stosb					; output string now filled with zeros
	dec      edi					; will keep zero in last element
	dec      edi					; edi now points at 2nd to last elemennt

	mov      esi, integer_address			; esi points to address of integer to write
	mov      ecx, MAX_OUT_LEN
	dec      ecx					; ecx = MAX_OUT_LEN - 1 b/c keep zero at end

; Check for sign of integer value
	mov      sign_one, 1				; intialize to +1. Will change to -1 if needed
	mov      eax, [esi]
	cmp      eax, 0
	jge      sign_val_stored			; if integer is positive, keep sign_one = +1
	mov      sign_one, -1				; if integer is neg, change sign_one to -1
sign_val_stored:

; Integer to ascii conversion algorithm
	std						; direction = backward
	mov      int_value, eax				; initialize intermediate value
find_next_string_element:
	mov      eax, int_value				; eax already equals int_value @ start of 1st loop, but not others
	cdq						; sign extend eax to edx.
	mov      ebx, 10
	idiv	 ebx
	mov      int_value, eax				; quotient saved in int_value.
	imul	 edx, sign_one				; if remainder is neg, change to positive
	add      edx, 48				; convert (always positive) remainder to ascii code
	mov      eax, edx				; ascii code to eax (< 10d, so fits in al)
	stosb						; write ascii code to string array and dec edi
	cmp      int_value, 0				; if quotient = 0, done converting digits..
	je       done_with_num_digits			; ...so exit loop
	loop     find_next_string_element
done_with_num_digits:

; Determine if need to write a '-'
	cmp      sign_one, 1
	jne      store_minus_sign
	inc      edi					; if no "-" needed, move edi to start of string
	jmp      ready_to_write

store_minus_sign:
	mov      al, 45
	mov      [edi], al

ready_to_write:
	displayString edi

	ret
writeVal ENDP


;-----------------------------------------------------------------------------------
; computeSumAndMean
; Computes the sum and mean of a list of integers stored in an array.
;
; Receives:			array_mean_address = address where mean value gets saved
;				array_sum_address = address where sum value gets saved
;				array_length = number of elements in array
;				array_address = address of array (1st element)
;
; Returns:			None
;
; Preconditions:		Calling procedure pushes in following order:
;				array_address, array_length, array_sum_address,
;				array_mean_address
;
; Post-conditions:		Mean value saved at array_mean_address, sum saved at
;				array_sum_address.
;
; Registers Changed:		None
;-----------------------------------------------------------------------------------

computeSumAndMean PROC USES ebx ecx edx esi edi,
	array_mean_address:PTR DWORD,
	array_sum_address:PTR DWORD,
	array_length:DWORD,
	array_address:PTR DWORD

	mov      ebx, 0					; ebx will be the accumulator
	cld						; direction = forward
	mov      esi, array_address			; esi points to 1st element in intege list
	mov      ecx, array_length			; set loop counter

; Calculate Sum
next_array_element:
	lodsd						; current element to eax and advance esi to next
	add      ebx, eax				; add current element to accumulator
	loop     next_array_element
	mov      edi, array_sum_address
	mov      [edi], ebx				; save sum to memory

; Calculate mean
	mov      eax, ebx
	cdq
	idiv     array_length				; eax = quotient, edx = remainder
	cmp      edx, 0
	jge      properly_rounded			; floor div means no change if dividend is positive or 0

; Rounding of mean if remainder is neg
	dec      eax					; remainder < 0 means sum was neg and need to round down

properly_rounded:
	mov      edi, array_mean_address
	mov      [edi], eax

	ret
computeSumAndMean ENDP


;-----------------------------------------------------------------------------------
; farewell
; Says goodbye
;
; Receives: 			byebye_address = address of string with Goodbye message
;
; Returns:			None
;
; Preconditions:		Calling procedure pushes byebye_address to stack
; 				immediately prior to calling.
;
; Post-conditions:		Farewell message displayed to screen
;
; Registers Changed:		None
;-----------------------------------------------------------------------------------
farewell PROC USES edx,
	byebye_address:PTR DWORD

	displayString byebye_address		 	; Use macro
	call     CrLf

	ret
farewell ENDP



END main
