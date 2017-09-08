#!/bin/sh

case $1 in
	out-nv) swipl -s falten.pl -g "fold(out,$2,X,Y),write(X),halt." | python3 falten.py;;
	out-dv) swipl -s falten.pl -g "fold(out,$2,X,Y),write(Y),halt." | python3 falten.py;;
	in-nv) swipl -s falten.pl -g "fold(in,$2,X,Y),write(X),halt." | python3 falten.py;;
	in-dv) swipl -s falten.pl -g "fold(in,$2,X,Y),write(Y),halt." | python3 falten.py;;
esac
