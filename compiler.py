# slightly modified from this project: https://github.com/tayler6000/BenEater8BitAssembler

import argparse
import base64
import io

commands = { b"NOP":0b00000000, b"LDA":0b00010000, b"ADD":0b00100000,
             b"SUB":0b00110000, b"STA":0b01000000, b"LDI":0b01010000,
             b"JMP":0b01100000, b"JC":0b01110000,  b"HLT":0b11110000 }

parsed = []
labels = {}

def parse(args):
  with open(args.in_file, 'rb') as f:
    for line in f:
      line = line.replace(b'\r', b'')
      line = line.replace(b'\n', b'')
      if line == b'' or line.strip(b' ') == b'':
        continue
      label = True
      command = ''
      argument = ''
      
      if line[0] == 32: # If the first char is a space
        label = False
        line = line.strip(b' ')
      line = line.split(b' ')
      if not len(line) == 2:
        line.append(None)
      
      if label and str(line[0], 'utf8')[-1] != ':':
        raise(Exception("Improper label: '"+str(line[0], 'utf8')+"' Did you mean: '"+str(line[0], 'utf8')+":'?"))
      
      parsed.append({'label':label, 'command':line[0], 'argument':line[1]})

def getInt(arg):
  if str(arg, 'utf8')[0] == '$':
    arg = arg.strip(b'$')
    if len(arg) == 1:
      arg = "0"+str(arg, 'utf8')
    arg = arg.upper()
    return ord(base64.b16decode(arg))
  elif arg in labels:
    return labels[arg]
  else:
    return int(arg)
    
def lex(args):
  program = io.BytesIO()
  counter = 0
  for x in parsed:
    if x['label']:
      labels[x['command'].strip(b':')] = counter
      continue
    counter += 1
  
  counter = 0
  for x in parsed:
    if x['label']:
      continue
    
    if str(x['command'], 'utf8')[0] == '.':
      if x['command'] == b'.org':
        counter = getInt(x['argument'])
        continue
      elif x['command'] == b'.word':
        program.seek(counter, 0)
        program.write(bytes([getInt(x['argument'])]))
        continue
    
    if not x['command'] in commands:
      raise(NotImplementedError("Unkown Operation: '"+str(x['command'], 'utf8')+"'"))
    
    if x['argument'] != None:
      arg = x['argument']
      try:
        program.seek(counter, 0)
        program.write(bytes([commands[x['command']] | getInt(x['argument'])]))
        counter += 1
        continue
      except:
        raise(Exception("Invalid argument: "+str(x['command']+b" "+x['argument'], 'utf8')))
    else:
      program.seek(counter, 0)
      program.write(bytes([commands[x['command']]]))
      counter += 1
      continue
  
  
  with open(args.o, 'wb') as f:
    program.seek(0,0)
    my_hexdata = program.read().hex()
    scale = 16 ## equals to hexadecimal
    num_of_bits = 8
    mybin = bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    # f.write(program.read())
    # f.write(mybin)
    padded = mybin.zfill(163)
    objectified = [*padded]
    # mybytes = str.encode(mybin)
    mybytes = str.encode( str( objectified ) )
    f.write(mybytes)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Assembler for Ben Eater's 8-bit computer. https://eater.net/8bit")
  parser.add_argument('in_file', type=str, help='The file you want to assemble')
  parser.add_argument('-o', metavar="out_file", type=str, help='The file you want to output to.  Default is out.bin', default="out.bin")

  arguments = parser.parse_args()
  parse(arguments)
  lex(arguments)
  print("Done.")
