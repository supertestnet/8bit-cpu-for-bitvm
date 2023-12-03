#!/bin/bash

input=$(awk '{print}')
json=($(echo $input | jq .[]))

printf \
"program counter\n"\
"${json[0]}${json[1]}${json[2]}${json[3]}\n"\
"microinstruction counter\n"\
"${json[4]}${json[5]}${json[6]}\n"\
"memory address register\n"\
"${json[7]}${json[8]}${json[9]}${json[10]}\n"\
"carry out\n"\
"${json[11]}\n"\
"register A\n"\
"${json[12]}${json[13]}${json[14]}${json[15]}${json[16]}${json[17]}${json[18]}${json[19]}\n"\
"register B\n"\
"${json[20]}${json[21]}${json[22]}${json[23]}${json[24]}${json[25]}${json[26]}${json[27]}\n"\
"instruction register\n"\
"${json[28]}${json[29]}${json[30]}${json[31]}${json[32]}${json[33]}${json[34]}${json[35]}\n"\
"ram\n"\
"${json[36]}${json[37]}${json[38]}${json[39]}${json[40]}${json[41]}${json[42]}${json[43]}\n"\
"${json[44]}${json[45]}${json[46]}${json[47]}${json[48]}${json[49]}${json[50]}${json[51]}\n"\
"${json[52]}${json[53]}${json[54]}${json[55]}${json[56]}${json[57]}${json[58]}${json[59]}\n"\
"${json[60]}${json[61]}${json[62]}${json[63]}${json[64]}${json[65]}${json[66]}${json[67]}\n"\
"${json[68]}${json[69]}${json[70]}${json[71]}${json[72]}${json[73]}${json[74]}${json[75]}\n"\
"${json[76]}${json[77]}${json[78]}${json[79]}${json[80]}${json[81]}${json[82]}${json[83]}\n"\
"${json[84]}${json[85]}${json[86]}${json[87]}${json[88]}${json[89]}${json[90]}${json[91]}\n"\
"${json[92]}${json[93]}${json[94]}${json[95]}${json[96]}${json[97]}${json[98]}${json[99]}\n"\
"${json[100]}${json[101]}${json[102]}${json[103]}${json[104]}${json[105]}${json[106]}${json[107]}\n"\
"${json[108]}${json[109]}${json[110]}${json[111]}${json[112]}${json[113]}${json[114]}${json[115]}\n"\
"${json[116]}${json[117]}${json[118]}${json[119]}${json[120]}${json[121]}${json[122]}${json[123]}\n"\
"${json[124]}${json[125]}${json[126]}${json[127]}${json[128]}${json[129]}${json[130]}${json[131]}\n"\
"${json[132]}${json[133]}${json[134]}${json[135]}${json[136]}${json[137]}${json[138]}${json[139]}\n"\
"${json[140]}${json[141]}${json[142]}${json[143]}${json[144]}${json[145]}${json[146]}${json[147]}\n"\
"${json[148]}${json[149]}${json[150]}${json[151]}${json[152]}${json[153]}${json[154]}${json[155]}\n"\
"${json[156]}${json[157]}${json[158]}${json[159]}${json[160]}${json[161]}${json[162]}${json[163]}\n"
# for debugging, uncomment the last 2 lines and add a backslash at the end of the one just above this comment
# "bus\n"\
# "${json[164]}${json[165]}${json[166]}${json[167]}${json[168]}${json[169]}${json[170]}${json[171]}\n"