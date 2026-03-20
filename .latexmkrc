$out_dir = 'compilation';
$aux_dir = 'compilation';

# Allow latexmk to find local style files moved out of root.
$ENV{'TEXINPUTS'} = './compilation/local_sty//:' . ($ENV{'TEXINPUTS'} // '');
