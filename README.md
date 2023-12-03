# 8bit cpu for bitvm
Write bitvm programs without learning circuit diagrams

# What is this?
This project contains a boolean logic circuit that emulates a turing complete 8 bit cpu that can run in bitvm. It also contains a debugger and state machine visualizer I wrote in python. If I can just write a compiler for it, coders will be able to program bitvm in an Assembly language rather than having to manually craft ever more complex boolean logic circuits.

# What is the status?
Every component of the cpu has been successfully tested. The last thing I successfully tested was a conditional jump instruction I wrote for its Assembly decoder, which makes the cpu turing complete. It currently supports 9 Assembly instructions documented below. So the status is: you can write programs in Assembly (using only the commands it currently supports), manually convert them to binary (I don't have a compiler yet), store them in RAM, run the computer, read the results it produces, and (I haven't tested this part yet) even lock up some bitcoins so that they can only be unlocked by your counterparty if he or she runs your program with inputs that produce some results you want.

However, all of that assumes you can do something useful in only one clock cycle, which is probably not usually true. Emulating and automating clock cycles will be a challenge for me and I expect it to take an additional week. Before I automate it, I will have to do some tests of the circuit by copy-pasting the full circuit several times, manually resetting the "input" wires each time so that they point at the output gates of the previous copy of the circuit. That will be a real chore if I have to do that e.g. dozens of times per test.

I hope to write some javascript to automate that so I can produce a version of the cpu that runs for like a thousand cycles or something, and I'll also need to write some javascript to decode bytes of RAM from 1s and 0s into something a human can understand -- like sprites on a screen, or text on a command prompt. Then I will need to document how to write and test programs for this cpu and show some examples that will hopefully inspire creativity in others to find out the limits of this cpu, or even make a better one.

# Supported commands
```
0. NOP -- do nothing
1. LDA -- load a value from ram into register A
2. ADD -- put the sum of registers A and B in register A
3. SUB -- put the difference of registers A and B in register A
4. STA -- store register A in ram
5. LDI -- load a value directly into register A (not from ram)
6. JMP -- jump to another instruction
7. JIC -- jump to another instruction if the carry bit is set, that is, if register A overflowed during computation of the previous instruction (this allows for "bounded loops" so that the cpu can run a loop for X number of times and then break out of it)
8. HLT -- stop the computer (must be entered twice)
```

Commands 1, 4, 5, and 6 take parameters. After specifying the command, give a number 0-15. Commands 1 and 4 use this number to set the ram to that byte, which it then loads into A (LDA) or overwrites with the contents of A (STA). Command 5 puts the number you specify directly into register A (usually it's a 1 or a 0 but it can be anything from 0 to 15). Commands 6 and 7 uses this number to determine which Assembly instruction you want it to jump to.

# Sample programs

## Count forever

The following program initializes the A register to 0 and then begins an incrementation loop, incrementing that register by 1 repeatedly. It gets stuck in this loop until the cpu stops cycling. In an ideal world, would be never, it would never stop cycling, but on bitcoin, it must stop before 2^128 cycles go by because bitcoin addresses don't have enough tapleaves to make more cycles than that.

Here it is in Assembly:

```
LDI 3
STA 15
LDI 0
ADD 15
STA 14
JMP 3
```

**Explanation of the above program**

`LDI 3` - initialize register A with the value 3
`STA 15` - then store that in byte 15 of ram
`LDI 0` - then reset A to 0
`ADD 15` - then add whatever is in byte 15 of ram to A (so add 3+0)
`STA 14` - then store whatever is in A in byte 14 of ram
`JMP 3` - go back to ADD 15 and loop

Here is the binary:

```
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,1,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
```

## Bounded loop test

The following program initializes the A register to a high value (252) and then begins enters an incrementation loop, incrementing that register by 1 repeatedly. It would get stuck in that loop forever, except that the JIC instruction causes it to depart the loop with Register A overflows due to being too small to hold the number 256. The JIC flag thus breaks it out of the loop, skipping to an instruction that stores the contents of the A register (which are now 0 due to the overflow) and halts the cpu.

Here it is in Assembly:

```
LDI 1
STA 14
LDA 15
ADD 14
JIC 6
JMP 3
STA 15
HLT
HLT
```

**Explanation of the above program**

`LDI 1` - initialize register A with the value 1
`STA 14` - then store that in byte 14 of ram
`LDA 15` - then put whatever is in byte 15 of ram in A (this makes it 252 because I booted the cpu with byte 15 already set to 252)
`ADD 14` - then add whatever is in byte 14 of ram to A (so add 252+1)
`JIC 6` - if the carry bit is set (i.e. if A overflowed) jump to the 7th instruction (which, counting from 0, is instruction 6)
`JMP 3` - go back to ADD 14 and loop (this instruction gets skipped once the A register overflows, thus letting us break out of the loop)
`STA 15` - then store whatever is in A in byte 15 of ram
`HLT` - this stops the computer
`HLT` - but it needs to be repeated twice because I'm not very good at making computers yet

Here it is in binary (with the 15th byte of RAM initialized to 252, not documented in the Assembly code)

```
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,1,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0]
```

# Big caveat
This cpu only has 16 bytes of ram. Don't expect to be validating bitcoin signatures or syncing a light client in it -- 16 bytes of ram isn't enough for anything but proofs-of-concept. You can demonstrate that bitvm is turing complete (and therefore so is bitcoin, since bitvm is a layer of bitcoin) but you probably can't do anything useful til someone makes a better cpu for bitvm with more ram. Consider that a challenge -- both the "make a better one" part and the "you can't do anything useful with this" part. I'd love to be proven wrong about that last one!

# What was your inspiration?
I had several inspirations. One of them came from making fun of ethereum's virtual machine one day. I joked that it isn't powerful enough to be a "world computer" (as some of the early hype claimed it was) because it only has about as much processing power as a gameboy. And then I realized that's not something to scoff at, that's super cool. And how cool would it be if *I* can emulate the original gameboy's cpu in bitvm and give people a way to validate whether someone successfully ran a gameboy ROM on bitcoin. If that's possible, you could lock up some bitcoins for someone that they can only take if they prove they beat you in [Doom](https://www.youtube.com/shorts/IXA1crHYPJE). How awesome would that be! So I started learning about the gameboy's cpu to see if it is feasible to emulate it in bitvm.

While researching the gameboy I realized that I know next to nothing about programming at that low level -- i.e. I don't know how to design a boolean logic circuit capable of running programs written in a programming language like Assembly. So I started learning about 8bit computer design (the gameboy uses an 8bit cpu) from [this video series](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU) by Ben Eater, and, since -- for every part of the design process -- he gives you direct instructions with helpful visuals and hands-on examples, I found I could follow his instructions in a circuit board simulator called [Logisim](http://www.cburch.com/logisim/).

I also started making Ben's examples my own by tweaking them for use in bitvm. For example, I took one of the early circuits I produced (an 8 bit "alu" or arithmetic and logic unit) and made a [github project](https://github.com/supertestnet/8bit-alu-for-bitvm) for it where I included not only my logisim file but a logically-equivalent circuit that I wrote using python's circuit library, which I then exported into bristol fashion using python's Bristol Fashion Circuit Library. I also successfully ran a closely related 8bit adder in bitvm that I also produced while following Ben Eater's instructions.

# What's next?

Now that the cpu works I hope to document it, write some example programs, and help inspire others to write creative programs for it. Hopefully that will attract the attention of some smarter developers who can design *better* cpus for it -- I dream of a 16 bit cpu and then a 32 bit cpu capable of running the linux operating system and any linux program. Imagine writing smart contracts for bitcoin in popular, modern languages like javascript or python. I don't think we're anywhere near there yet but we're probably closer than we've ever been, and I can't wait to see what's next.
