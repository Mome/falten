%——————————————————————————————————————————————————————————————————
% cross-fold algorithm, generating the folded edges in bar-bra notation
%——————————————————————————————————————————————————————————————————
%
% Bar-bra notation:
%
% bars "|" denote open edges,
% brackets "()" denote closed ones
% a semicolon is used to separate independent sides 
% (for the DV, cf. example below)
%
% imagine this string as depicting the uppermost ends of the side view of a 
% fold,joining these with concentric arcs (not crossing the semicolon)
% produces the side view again.
%
% e.g. "||()" would denote:
%
% ││╭╮
% ││││
% │╰╯│
% ╰──╯
%
% and "||;||":
%
% ││ ││
% ╰╯ ╰╯
%
%——————————————————————————————————————————————————————————————————
%
% fold/4 recursively generates both sides of the Num-th fold
%
% its first argument has to be either "out" or "in" and determines whether
% an out-fold or in-fold will be produced
%
%——————————————————————————————————————————————————————————————————
% (NV == nested side, DV == double side)
%——————————————————————————————————————————————————————————————————

% base case: (for out- & in-fold) the 1-fold is "||" and "|;|"
fold(_,1,"||","|;|").


% recursive out-fold
fold(out,Num,NV,DV) :- Num >= 2,
						DecrNum is Num - 1,
						fold(out,DecrNum,DecrNV,DecrDV),
						% build new out-folded NV from old DV
						new_nv(out,DecrDV,NV),
						% build new out-folded DV from old NV
						new_dv(out,DecrNV,DV).

% recursive in-fold
fold(in,Num,NV,DV) :-
						Num >= 2,
						DecrNum is Num - 1,
						fold(in,DecrNum,DecrNV,DecrDV),
						new_nv(in,DecrDV,NV),
						new_dv(in,DecrNV,DV).

%——————————————————————————————————————————————————————————————————
% generates NV of a fold based on the DV of the preceding fold

new_nv(_,"|;|","||||") :-	!.

new_nv(out,OldDV,NewNV) :-% split old DV at the semicolon
						split_string(OldDV,";","",[LeftOldDV,RightOldDV]),
						% get length of the right side of the old DV
						string_length(RightOldDV,LenRight),
						% integer-divide this length
						NumVs is LenRight // 2,
						% generate as many nested Vs (i.e. parens)
						vs(NumVs,NewVs),
						% concatenate: LeftOldDV,RightOldDV,NestedVs,single ()
						string_concat(LeftOldDV,RightOldDV,Part1),
						string_concat(Part1,NewVs,Part2),
						string_concat(Part2,"()",NewNV).

new_nv(in,OldDV,NewNV) :-% split old DV at the semicolon
						split_string(OldDV,";","",[LeftOldDV,RightOldDV]),
						% get length of the left side of the old DV
						string_length(LeftOldDV,LenLeft),
						% integer-divide this length
						NumVs is LenLeft // 2,
						% generate as many nested Vs
						vs(NumVs,NewVs),
						% concatenate: LeftOldDV,RightOldDV,single (),NestedVs
						string_concat(LeftOldDV,RightOldDV,Part1),
						string_concat(Part1,"()",Part2),
						string_concat(Part2,NewVs,NewNV).


%——————————————————————————————————————————————————————————————————
% generates DV of a fold based on the NV of the preceding fold

new_dv(out,OldNV,NewDV) :-% the new DV is the preceding NV,
						   % preprended by "||;" (a single, open V)
						string_concat("||;",OldNV,NewDV).

new_dv(in,OldNV,NewDV) :-% the new DV is the preceding NV,
						  % appended by ";||" (a single, open V)
						string_concat(OldNV,";||",NewDV).
%——————————————————————————————————————————————————————————————————
% Helpers:
%——————————————————————————————————————————————————————————————————
% Generate #Num numbers of nested parens

vs(0,"").
vs(Num,Vs) :-		vs_helper(Num,V1List,V2List),
					atomic_list_concat(V1List,V1s),
					atomic_list_concat(V2List,V2s),
					string_concat(V1s,V2s,Vs).

%——————————————————————————————————————————————————————————————————
% helper for vs/2, accumulating left- and right-parens tail-recursively
vs_helper(0,[],[]).


vs_helper(Num,["("|Lparens],[")"|Rparens]):- 	
											NewNum is Num - 1,
											vs_helper(NewNum,Lparens,Rparens).
%——————————————————————————————————————————————————————————————————
