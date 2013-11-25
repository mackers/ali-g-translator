#!/usr/bin/perl

#########################################
#
# Da Ali G Translata
#
# WARNING: VERY OLD, VERY CRAPPY CODE!!!
#
#########################################

##variables##
$allowwww=0;
$path="/home/mackers/www/alig";
$url="http://mackers.com/alig";
$script="alig.cgi";
#############

use LWP::Simple;
#comment the above if this library is not present.

&ReadParse;
srand;
&setWords;
$path=~s/(\/)$//;
$url=~s/(\/)$//;

($cgi_lib'version = '$Revision: 2.8 $') =~ s/[^.\d]//g;

$cgi_lib'maxdata    = 131072;    # maximum bytes to accept via POST - 2^17
$cgi_lib'writefiles =      0;    # directory to which to write files, or
$cgi_lib'filepre    = "cgi-lib"; # Prefix of file names, in directory above
$cgi_lib'bufsize  =  8192;    # default buffer size when reading multipart
$cgi_lib'maxbound =   100;    # maximum boundary length to be encounterd
$cgi_lib'headerout =    0;    # indicates whether the header has been printed

print "Content-type:text/html\n\n";

$_ = $in{'text'};
if ((/^((http)|(www))/) && ($allowwww || $in{'allowwww'})){

$in{'text'} =~ s/(\n|\r)//g;
@html = &absolute($in{'text'});
@images = <$path/images/*>;

#print join (";;",@html);

foreach $line (@html) {
  unless ($line=~/(<.*?>)/s) {
    $line = &translate($line);
  } else {
    if (($line=~/<img.*http/i)&&(rand(3)>2)){
      my $image = $images[rand($#images)];
      $image =~ s/$path\//$url\//i;
      $line =~ s/(<img src=").*?"/$1$image"/i;
      $line =~ s/((width=)|(height=))[^ ]*//ig;
    }
    $line =~ s/((<frame.*?src=")|(href="))http/$1$url\/$script?text=http/gi;
  }
  print $line;
}

} else {

unless ($in{'text'}) {
$out = "Enter da text to translate below:" if ($string eq "");
$string = ""
} else {
$string = $in{'text'};
#$string =~ s/(\r|\f)//;
$output = &translate($string);
$out = $output;
$out =~ s/\n/<br>/g;
$out =~ s/(<br>)$//g;
}
open (TOP, "$path/header.html");
while (<TOP>){print $_}
close (TOP);
print "<form action=\"$url/$script\" method=get>\n";
print "<table border=1 bordercolor=\"#FFFF00\" align=center width=\"100%\"";
print " cellpadding=5 cellspacing=0><tr><td>\n";
print "<font color=\"#FFFF00\" face=\"Arial\" size=\"2\">";
print "<b>$out\n</b><br><br>\n";
print "</font>\n</td></tr></table>\n<br>\n<center>\n";
print "\t\t<textarea name=text rows=7 cols=35>";
print "$string";
print "</textarea><br>\n";
print "\t\t<input type=submit value=\"Translate\">\n";
print "\t\t</form>\n</center>\n";
open (BOT, "$path/footer.html");
while (<BOT>){
  print $_;
}
close (BOT);
}

sub logthis {
open (CMD, "nslookup $ENV{'REMOTE_ADDR'} |");
  while (<CMD>) {
    $ns = $_ if (/Name/);
  }
close (CMD);

$ns =~ s/(Name:)|( )|(\t)//g;
$ns =~ s/\n//g;

open (OUT,">>$path/log");
my $log = $_[0] . "\n\n";
$log =~ s/\r//g;
$log =~ s/\n\n/\n/g;
$time = gmtime;
print OUT "--- $time $ns ".$ENV{'HTTP_REFERER'}." ---\n";
print OUT $log;
close (OUT);
}

sub translate {
$return = "";
foreach (split(/\n/,$_[0])) {
if (/^(<)/) {
  print $_;
} else {
  #chop();
  $sentence = $_;
  $sentence = &changePhrase($sentence);
  foreach $word (split(/ /,$sentence)) {
    $word =~ s/()//;
    $word =~ s/([.?!,])$//;
    $punctuation = $1;
    $word=~s/(s)$/$+/i;
    $wordSLess=$`;
    $word=~s/(ing)$/$+/i;
    $wordIngLess=$`;
    $word=~s/(en)$/$+/i;
    $wordEnLess=$`;
    $word=~s/(\'s)$/$+/i;
    $wordASLess=$`;
    if (&straightChange($word,"")) {
      $aliVersion = &straightChange($word,"");
    } elsif (&straightChange($wordSLess,"s")) {
      $aliVersion = &straightChange($wordSLess,"s");
    } elsif (&straightChange($wordIngLess,"ing")) {
      $aliVersion = &straightChange($wordIngLess,"ing");
    } elsif (&straightChange($wordEnLess,"en")) {
      $aliVersion = &straightChange($wordEnLess,"en");
    } elsif (&straightChange($wordASLess,"\'s")) {
      $aliVersion = &straightChange($wordASLess,"\'s");
    } else {
      $aliVersion = &changeSpelling($word);
    }
    $punctuation = &changePunctuation($punctuation);
    $return.="$aliVersion$punctuation ";
  }
  #print "\n";
  $return.="\n";
}
}
$return;
}

sub straightChange {
  $_ = "";
  $_ = $alight{(lc $_[0])};
  if ($_) {
    if (/\//) {
      @values = split(/\//);
      $rint = rand(scalar @values);
      $_ = $values[$rint] . $_[1];
    } else {
      $_ . $_[1];
    }
  } else {
    0;
  }
}

sub changeSpelling {
  $_ = $_[0];
#replaces ing at end of word with in
  s/(ing)$/in/i;
#replaces th at end of word f
  s/(th)$/f/i;
#replaces en at end of word with un
  s/(([bcdfghjklmnpqrstvwxyz])en)$/$2un/i;
#replaces er at end of word with a
  s/(([bcdfghjklmnpqrstvwxyz])er)$/$2a/i;
#drops h from start of word
  if ((rand(2) < 2) && (/(i)$/)){
    s/^(h)//i;
  }
#replaces any [vowel]ck with [vowel[k]
  s/([aeiou]ck)/$1/i;
  $t = $1;
  if ($1) {
    $t =~ s/c//i;
    s/[aeiou]ck/$t/i;
    $t = "";
  }
#replaces [vowel] at first word with h[vowel]
  if ((rand(4) >= 3) && (/^(i|a|e|o|a)/)){
    $_ = "h" . $_;
  }
#if word > x chars add weird syllables
  if (length($_) > 8) {
    $ook = substr($_,length($_)/3);
    $ook =~ s/([aeiou])([bcdfghjklmnpqrstvwxyz])([aeiou])([bcdfghjklmnpqrstvwxyz])([aeiou])/$1$4$3$2$5/i;
    $_ = substr($_,0,length($_)/3).$ook;
  }
  $_;
}

sub changePhrase {
  $_ = $_[0];
  foreach $key (keys %phrases) {
    if (/$key/i){
      $value = $phrases{$key};
      $ook = $1;
      $value =~ s/ \$ / $ook /;
      s/$key/$value/gi;
    $changed = 1;
    } else {
    $changed = 0;
    }
  }
  $_;
}

sub changePunctuation {
  $_ = $_[0];
  local $qs = ". Is it coz I is black?";
  local $es = ". Boyakasha!";
  if (rand(3) > 2) {
    s/\?/$qs/;
    s/\!/$es/;
  }
  local $ps = ", man.";
  if (rand(10) >9) {
    s/\./$ps/;
  }
  $_;
}

sub setWords {
%alight = (
"hiya" => "alo",
"language" => "lingo",
"hows" => "how is",
"how's" => "how is",
"animal" => "aminal",
"slut" => "mingin bitch",
"goods" => "goods",
"thanks" => "fanks",
"what\'s" => "wus",
"slag" => "mingin bitch",
"boyfriend" => "main man",
"you\'re" => "yous is",
"pleasure" => "sweet bitching",
"partner" => "bitch",
"willy" => "mr biggy",
"hole" => "batty",
"bollox" => "balls",
"goodlooking" => "fit",
"faggot" => "batty boy",
"faggott" => "batty boy",
"knob" => "dong",
"prostitute" => "ho",
"whore" => "ho",
"hooker" => "ho",
"dyke" => "feminist",
"humped" => "boned",
"humps" => "bones",
"funny" => "wicked",
"fun" => "wicked",
"flat" => "turf",
"insult" => "dis",
"insults" => "disses",
"insulting" => "dissing",
"insulted" => "dissed",
"document" => "bit of paper",
"in" => "on",
"support" => "help",
"prepare" => "make",
"prepared" => "made",
"centre" => "house",
"center" => "house",
"curse" => "say a swear word",
"curses" => "sez swear words",
"cursing" => "saying swear words",
"cursed" => "sed swear words",
"apartment" => "turf",
"words" => "lingo",
"sentences" => "lingo",
"bedsit" => "turf",
"irish" => "sound",
"clothes" => "threads",
"northside" => "westside",
"cap" => "tommy",
"police" => "constalubury",
"cops" => "constalubury",
"constabulary" => "constalubury",
"boys" => "main men",
"seen" => "checked",
"birds" => "bitches",
"bestfriend" => "main man",
"situation" => "story",
"gaelic" => "gay lick",
"gailic" => "gay lick",
"folk" => "geezers",
"pub" => "boozer",
"dirty" => "mingin",
"mum" => "mam",
"brother" => "bruver",
"sweet" => "wicked",
"melon" => "babylon",
"hooter" => "babylon",
"boob" => "babylon",
"tittie" => "babylon",
"honker" => "babylon",
"schedule" => "sex life",
"timetable" => "sex life",
"speed" => "speeden",
"filthy" => "mingin",
"best" => "wickedest",
"lunch" => "grub",
"period" => "blob",
"tv" => "telly",
"moron" => "chief",
"idiot" => "chief",
"feet" => "feets",
"foot" => "foots",
"relaxation" => "chillin",
"clit" => "love button",
"clitoris" => "love button",
"rac" => "ruc",
"dickhead" => "chief",
"attractive" => "fit",
"fag" => "batty boy",
"cute" => "fit",
"ride" => "bang",
"butt" => "batty",
"bang" => "bone",
"dumass" => "chief",
"funniest" => "wickedist",
"fat" => "large",
"horrible" => "mingin",
"wales" => "the biggest dick in da ocean",
"marajuana" => "erbal remedy",
"organisation" => "crew",
"anus" => "batty",
"individual" => "main man",
"manager" => "main man",
"dinner" => "grub",
"suffer" => "moan",
"suffers" => "moans",
"guy" => "geezer",
"pregnant" => "preggers",
"gift" => "pressie",
"toilet" => "bog",
"crapper" => "bog",
"shitter" => "bog",
"pisser" => "bog",
"quid" => "squid",
"pound" => "squid",
"millenium" => "minnenium",
"lend" => "borrow",
"give" => "borrow",
"sell" => "borrow",
"borrow" => "steal",
"coins" => "coppers",
"loo" => "bog",
"lav" => "bog",
"lavatory" => "bog",
"service" => "mend",
"scotland" => "wales",
"fucking" => "well",
"fox" => "lady",
"glasses" => "yellow sunglasses",
"hassle" => "aggro",
"stress" => "aggro",
"break" => "chill",
"jump" => "hop",
"jumped" => "hopped",
"food" => "grub",
"hospital" => "hostipal",
"conservative" => "constervative",
"thanks" => "big up",
"granny" => "nan",
"grandmother" => "nan",
"gran" => "nan",
"uncle" => "uncle jamal",
"beautiful" => "wicked",
"craic" => "crack",
"shaven" => "shaven haven",
"hairy" => "mingin",
"coat" => "tommy hilfinger",
"fool" => "batty boy",
"coppers" => "pigs",
"annoying" => "pissin",
"beast" => "mr biggy",
"law" => "pigs",
"fantastic" => "wicked",
"bbc" => "telly",
"barn" => "farm",
"work" => "wurk",
"wife" => "bitch",
"jail" => "inside",
"prison" => "inside",
"gaol" => "inside",
"lunchtime" => "grubtime",
"dinnertime" => "grubtime",
"bored" => "chilled",
"chilled" => "ambient",
"music" => "tunes",
"keen" => "wicked",
"scientist" => "skientist",
"horse" => "aminal",
"tit" => "babylon",
"slag" => "bitch",
"mother" => "mam",
"erection" => "bone",
"freak" => "bitch",
"dead" => "stiff",
"coke" => "craic",
"westside" => "staines",
"bent" => "batty",
"dude" => "man",
"whales" => "da biggest dick in the ocean",
"minge" => "punanni",
"minj" => "punanni",
"enemy" => "emeny",
"enemies" => "emenies",
"brill" => "wicked",
"brilliant" => "wicked",
"breast" => "babylon",
"intelligent" => "brainiest",
"clever" => "brainiest",
"skilled" => "brainiest",
"cunning" => "brainiest",
"quick" => "quicrest",
"home" => "westside",
"bisexual" => "trisexual",
"asses" => "batties",
"joint" => "spliff",
"trouble" => "aggro",
"shagger" => "boner",
"sheep" => "aminal",
"massive" => "massiv",
"pretty" => "fit",
"boss" => "main man",
"definitely" => "for real",
"darling" => "bitch",
"darlin" => "bitch",
"queen" => "main bitch",
"rocks" => "is wicked",
"king" => "main man",
"asshole" => "batty hole",
"arsehole" => "batty hole",
"bumhole" => "batty hole",
"butthole" => "batty hole",
"butt" => "batty",
"handsome" => "wicked",
"jeep" => "auto",
"truck" => "auto",
"bird" => "bitch",
"gear" => "erbal remedy",
"drunk" => "a little bit ratted",
"cane" => "erbal remedy",
"spliff" => "erbal remedy",
"guy" => "boy",
"great" => "wicked",
"his" => "is",
"alright" => "aight",
"hello" => "alo",
"hi" => "alo",
"greeting" => "hear me now",
"greetings" => "hear me now",
"lover" => "bitch",
"welcome" => "hear me now, dis is",
"agent" => "asian",
"bottom" => "batty",
"bum" => "batty",
"ass" => "batty",
"arse" => "batty/exit",
"gay" => "batty boy",
"gays" => "batty boys",
"queer" => "batty boy",
"queers" => "batty boys",
"talking" => "bangin/natterin",
"speaking" => "bangin/natterin",
"shouting" => "bangin",
"talk" => "bang/natter",
"speak" => "bang/natter",
"shout" => "bang",
"absolutely" => "for real",
"wonderful" => "wicked",
"crap" => "mingin",
"heroin" => "gear",
"banged" => "boned",
"car" => "auto",
"love" => "dig",
"buy" => "purchase",
"matey" => "main man",
"smells" => "stinks",
"smell" => "stink",
"cow" => "bitch",
"pig" => "bitch",
"stupid" => "bit thick",
"thick" => "bit thick",
"balls" => "mr biggies",
"staines" => "me turf",
"men" => "bruvers",
"babe" => "fit bitch",
"friend" => "main man",
"studying" => "hangin",
"study" => "hang",
"cannabis" => "erbal remedy",
"mate" => "main man",
"chum" => "main man",
"very" => "well",
"nazies" => "commies",
"nazy" => "commy",
"commy" => "nazy",
"commies" => "nazies",
"techno" => "speed garage",
"hiphop" => "speed garage",
"indie" => "speed garage",
"pop" => "speed garage",
"rock" => "speed garage",
"jazz" => "speed garage",
"wank" => "crack one off",
"wanks" => "cracks one off",
"wanked" => "cracked one off",
"wanking" => "cracking one off",
"masturbate" => "crack one off",
"masturbates" => "cracks one off",
"masturbated" => "cracked one off",
"masturbating" => "cracking one off",
"situation" => "deal",
"bisexual" => "trisexual",
"bastard" => "bastid",
"club" => "cukabilly",
"happy" => "chilled",
"lad" => "main man",
"cheese" => "erbal remedy",
"neighbourhood" => "turf",
"neighbours" => "homies",
"nigger" => "bruver",
"poofter" => "batty boy",
"poof" => "batty boy",
"pouf" => "batty boy",
"skank" => "erbal remedy",
"wench" => "bitch",
"lady" => "bitch",
"i\'m" => "me is",
"groovy" => "wicked",
"blonde" => "fit",
"cigarette" => "fag",
"langer" => "dong",
"dong" => "knob",
"awful" => "mingin",
"hurt" => "is wrecked",
"person" => "main man",
"fenian" => "muslim",
"paddy" => "muslim",
"draw" => "erbal remedy",
"dog" => "aminal",
"cat" => "aminal",
"lovely" => "wicked",
"girlfriend" => "bitch",
"twat" => "minge/punanni",
"big" => "massiv",
"huge" => "massiv",
"gigantic" => "massiv",
"large" => "massiv",
"bunch" => "crew",
"everybody" => "me crew",
"hate" => "don\'t dig",
"dislike" => "don\'t dig",
"sexy" => "fit",
"sexiest" => "fittest",
"sexier" => "fitter",
"fart" => "trumpet",
"farts" => "trumpets",
"colleage" => "main man",
"pregnant" => "up da spout",
"bird" => "bitch",
"anal" => "batty",
"im" => "i is",
"screw" => "bone",
"most" => "mostest",
"test" => "da test",
"smelly" => "stinkin",
"worker" => "main man",
"coworker" => "main man",
"employee" => "main man",
"friends" => "boys",
"mates" => "boys",
"chums" => "boys",
"colleages" => "boys",
"workers" => "boys",
"home" => "turf",
"coworkers" => "boys",
"woman" => "bitch",
"girl" => "bitch",
"female" => "bitch",
"women" => "wimin/bitches",
"girls" => "bitches",
"ladies" => "bitches",
"females" => "bitches",
"dozen" => "quillion",
"hundred" => "quillion",
"thousand" => "quillion",
"million" => "quillion",
"billion" => "quillion",
"chicken" => "chikun",
"team" => "crew",
"gang" => "crew",
"company" => "crew",
"squad" => "crew",
"clockwork" => "chocolate",
"relax" => "chill",
"enjoy" => "chill",
"loose" => "chill",
"slack" => "chill",
"rest" => "chill",
"unwind" => "chill",
"like" => "dig",
"tool" => "dong",
"fancy" => "dig",
"favour" => "dig",
"prefer" => "dig",
"enjoy" => "dig",
"glance" => "check",
"gaze" => "check",
"stare" => "check",
"gape" => "check",
"look" => "check",
"search" => "check",
"find" => "check",
"explore" => "check",
"discover" => "check",
"browse" => "check",
"peep" => "check",
"investigate" => "check",
"inspect" => "check",
"hunt" => "check",
"seek" => "check",
"probe" => "check",
"examine" => "check",
"inspect" => "check",
"arse" => "batty",
"vagina" => "flange/punanni",
"boys" => "bruvers",
"pussy" => "flange/punanni",
"cunt" => "flange/punanni",
"fanny" => "flange/puanni",
"muff" => "flange/punanni",
"lesbian" => "feminist",
"lesbianism" => "feminism",
"really" => "for real",
"truly" => "for real",
"especially" => "for real",
"positely" => "for real",
"uncommonly" => "for real",
"exceptional" => "fore real",
"thing" => "fing",
"here" => "ere",
"that\'s" => "innit",
"actual" => "hactual",
"hash" => "erbal remedy",
"hashish" => "erbal remedy",
"ganja" => "erbal remedy",
"blow" => "erbal remedy",
"sensi" => "erbal remedy",
"marijuana" => "erbal remedy",
"dope" => "erbal remedy",
"cocaine" => "erbal remedy",
"hot" => "spunky",
"money" => "mula",
"ugliest" => "mingiest",
"unsexy" => "mingiest",
"condom" => "rubber",
"weed" => "erbal remedy",
"homosexual" => "homosapien",
"homosexuals" => "homosapiens",
"homosapien" => "homosexual",
"blacks" => "bruvers",
"jesus" => "Jackie Chan",
"god" => "Jackie Chan",
"click" => "let it rip",
"enter" => "let it rip",
"angry" => "menstural",
"ugly" => "mingin/rank",
"rotten" => "mingin/rank",
"hated" => "mingin/rank",
"nasty" => "mingin/rank",
"protestant" => "muslim",
"protestants" => "muslims",
"catholic" => "muslim",
"catholics" => "muslims",
"muslim" => "catholics",
"penis" => "dong",
"cock" => "dong",
"dick" => "dong",
"nuts" => "balls",
"balls" => "biggies",
"baby" => "bitch",
"semen" => "orange juice",
"spunk" => "orange juice",
"sperm" => "orange juice",
"fight" => "ruk",
"argument" => "ruk",
"row" => "ruk",
"fights" => "ruks",
"arguments" => "ruks",
"rows" => "ruks",
"racist" => "racalist",
"racists" => "racalists",
"present" => "in da house",
"here" => "in da house",
"absent" => "not in da house",
"missing" => "not in da house",
"smiley" => "cheeky",
"specifically" => "pacifically",
"specif" => "pacific",
"exactly" => "pacifically",
"exact" => "pacific",
"racism" => "racalist",
"discrimination" => "racalist",
"RUC" => "RAC",
"compliment" => "respect",
"compliments" => "respects",
"things" => "fings",
"terrorism" => "terrerorism",
"terrorist" => "terrerorist",
"terrorist" => "terrerorists",
"fuck" => "ride the punanni",
"see" => "check",
"fucking" => "riding the punanni",
"shag" => "ride the punanni",
"shagging" => "ride the punanni",
"shagged" => "boned",
"favourite" => "bestest",
"favorite" => "bestest",
"ballix" => "balls",
"family" => "crew",
"loads" => "quillions",
"lots" => "quillions",
"want" => "dig",
"sleep" => "go to me julie",
"drug" => "erbal remedy",
"drugs" => "erbal remedies",
"town" => "turf",
"city" => "turf",
"country" => "turf",
"is" => "is",
"land" => "turf",
"my" => "me",
"that" => "dat",
"thats" => "dats",
"because" => "coz",
"strange" => "batty",
"old" => "batty",
"bizarre" => "batty",
"yes" => "aye",
"certainly" => "aye",
"the" => "da",
"good" => "wicked",
"dj" => "selecta",
"cool" => "wicked",
"nice" => "wicked",
"ok" => "wicked",
"fine" => "wicked",
"urinate" => "do a piss",
"urinates" => "does a piss",
"urinating" => "doing a piss",
"urinated" => "did a piss",
"bugger" => "bum",
"bumfuck" => "bum",
"bestfriend" => "main man",
"excellent" => "wicked",
"best" => "fittest",
"coolest" => "fittest",
"nicest" => "fittest",
"finest" => "fittest",
"man" => "geezer",
"bloke" => "geezer",
"dad" => "old geezer",
"yugoslavia" => "Newgoslavia",
"italy" => "Newgoslavia",
"mature" => "full bush",
"ripe" => "full bush",
"full" => "maximum",
"enormous" => "maximum",
"teenage" => "half bush",
"teenager" => "half bush",
"adolescence" => "half bush",
"adolescant" => "half bush",
"perfect" => "wicked",
"hungary" => "Newgoslavia",
"greece" => "Newgoslavia",
"austria" => "Newgoslavia",
"father" => "old geezer",
"this" => "dis",
"they" => "dey",
"other" => "udder",
"am" => "is",
"are" => "is",
"shit" => "plop",
"million" => "quillion",
"honey" => "bitch",
"trillion" => "quillion",
"youth" => "youf",
"been" => "bin",
"you" => "yous",
"bye" => "bo",
"luv" => "bitch",
"chick" => "bitch",
"bad" => "wicked",
"dodgy" => "batty",
"swiss" => "batty",
"grass" => "erbal remedy",
"goodbye" => "bo",
"good-bye" => "bo",
"seeya" => "bo",
"see-ya" => "bo",
"tired" => "wrecked",
"exhausted" => "wrecked",
"motor" => "auto",
"gorgeous" => "fit",
"penises" => "mr biggies",
"sad" => "down",
"upset" => "down",
"depressed" => "down",
"pork" => "bone",
"porked" => "boned",
"with" => "wiv",
"college" => "scool",
"school" => "scool",
"an" => "a",
"technology" => "bits",
"what" => "wot",
"sex" => "riding the punanni",
"i" => "me",
"computer" => "pooter"
);
%phrases = (
"jerk off" => "crack one off",
"haven\'t" => "ain\'t",
"hasn\'t" => "ain\'t",
"have not" => "ain\'t",
"has not" => "ain\'t",
"have never" => "ain\'t never",
"has never" => "ain\'t never",
"am gay" => "like it up both pipes",
"is gay" => "likes it up both pipes",
"well done" => "big up",
"pleased to meet you" => "big up to you",
"have sex" => "get jiggy",
"has sex" => "bones",
"having sex" => "riding the punanni",
"listen to me" => "hear me now",
"isnt it" => "innit",
"isn\'t it" => "innit",
"that's right" => "innit",
"what\'s up" => "whaddup",
"had" => "did have",
"i heard" => "me crew told me",
"i hear" => "word on da street",
"girl friend" => "bitch",
"i want" => "me would dig",
"i like" => "me would dig",
"that's correct" => "innit",
"i live in" => "me turf is",
"i\'m from" => "me turf is",
"a ride" => "fit",
"boy friend" => "main man",
"disc jockey" => "selecta",
"disk jockey" => "selecta",
"are you gay" => "do you like it up both pipes",
"backdoor burgler" => "batty boy",
"im from" => "me turf is",
"i come from" => "me turf is",
"make love" => "bone",
"what\'s up" => "wussup",
"whats up" => "wassup",
"good looking" => "fit",
"a joint" => "some erbal remedy",
"a spliff" => "some erbal remedy",
"a bent" => "a batty boy",
"tonight" => "a bit later on",
"smoking" => "toking",
"smokes" => "tokes",
"working" => "hangin",
"meeting" => "hangin",
"colleagues" => "crew",
"a smoke" => "a bit of erbal remedy",
"pissed off" => "aggro",
"im going home" => "me is heading westside",
"i\'m going home" => "me is heading westside",
"my home" => "westside",
"anal sex" => "batty boning",
"fuck off" => "chill",
"shut up" => "chill",
"go home" => "head westside",
"the hood" => "staines",
"what are you talking about" => "wot is yous bangin on about",
"i don\'t know" => "me don't have a clue",
"night club" => "cukabilly",
"disco" => "cukabilly",
"sinn fein" => "muslims",
"first class" => "the most bestest",
"class a" => "the most bestest",
"blow job" => "sweet mr biggy lovin",
"i like you" => "would you dig to get jiggy wiv mr biggy",
"i love you" => "would you dig to get jiggy wiv mr biggy",
"i fancy you" => "would you dig to get jiggy wiv mr biggy",
"like to have sex" => "dig to get jiggy wiv mr biggy",
"how are you feeling" => "is you wicked",
"make love" => "ride the punanni",
"my bed" => "the sack",
"big one" => "mr biggy",
"where do you live" => "where is yous turf",
"good looking" => "fit",
"going home" => "going westside",
"making love" => "riding the punanni",
"made love" => "boned",
"west side" => "me turf",
"a break" => "a chill pill",
"what time is it" => "keep it real and tell me da time",
"channel 4" => "telly",
"laid" => "jiggy",
"how do you do" => "is you wicked",
"how are you" => "is you wicked",
"how's it going" => "is you wicked",
"give me a ring" => "gimme a shout",
"i find you" => "i fink you is",
"Where do I live" => "where is me turf",
"what plans" => "what\'s the deal",
"oral sex" => "drinking from the bearded cup",
"have fun" => "chill",
"a pay rise" => "mo mula",
"are you going out" => "is you goin out to check some bitches",
"to the pub" => "down the boozer",
"looking at" => "checkin out",
"my name is (.*)" => "me name is \$ and i is a batty boy",
"my girlfriend is (.*)" => "me bitch is \$ , who i definitely would knob",
"my boyfriend is (.*)" => "me bitch is \$ , who i definitely would knob",
"my wife is (.*)" => "me bitch is \$ , who i definitely would knob",
"my husband is (.*)" => "me bitch is \$ , who i definitely would knob",
"i feel like" => "i fink i will be",
"he feels like" => "he finks he will be",
"she feels like" => "she finks she will be",
"that\'s not right" => "dat ain\'t right",
"slag off" => "dis",
"slags off" => "disses",
"slagged off" => "dissed",
"have a piss" => "do a piss",
"has a piss" => "does a piss",
"had a piss" => "did a piss",
"having a piss" => "doing a piss",
"slagging off" => "dissing",
"welcome to" => "hear me now, dis is"
);

}
# Perl Routines to Manipulate CGI input
# S.E.Brenner@bioc.cam.ac.uk
# $Id: cgi-lib.pl,v 2.8 1996/03/30 01:36:33 brenner Rel $
#
# Copyright (c) 1996 Steven E. Brenner  
# Unpublished work.
# Permission granted to use and modify this library so long as the
# copyright above is maintained, modifications are documented, and
# credit is given for any use of the library.
#
# Thanks are due to many people for reporting bugs and suggestions
# especially Meng Weng Wong, Maki Watanabe, Bo Frese Rasmussen,
# Andrew Dalke, Mark-Jason Dominus, Dave Dittrich, Jason Mathews

# For more information, see:
#     http://www.bio.cam.ac.uk/cgi-lib/


# ReadParse
# Reads in GET or POST data, converts it to unescaped text, and puts
# key/value pairs in %in, using "\0" to separate multiple selections

# Returns >0 if there was input, 0 if there was no input 
# undef indicates some failure.

# Now that cgi scripts can be put in the normal file space, it is useful
# to combine both the form and the script in one place.  If no parameters
# are given (i.e., ReadParse returns FALSE), then a form could be output.

# If a reference to a hash is given, then the data will be stored in that
# hash, but the data from $in and @in will become inaccessable.
# If a variable-glob (e.g., *cgi_input) is the first parameter to ReadParse,
# information is stored there, rather than in $in, @in, and %in.
# Second, third, and fourth parameters fill associative arrays analagous to
# %in with data relevant to file uploads. 

# If no method is given, the script will process both command-line arguments
# of the form: name=value and any text that is in $ENV{'QUERY_STRING'}
# This is intended to aid debugging and may be changed in future releases

sub ReadParse {
  local (*in) = shift if @_;    # CGI input
  local (*incfn,                # Client's filename (may not be provided)
	 *inct,                 # Client's content-type (may not be provided)
	 *insfn) = @_;          # Server's filename (for spooled files)
  local ($len, $type, $meth, $errflag, $cmdflag, $perlwarn);
	
  # Disable warnings as this code deliberately uses local and environment
  # variables which are preset to undef (i.e., not explicitly initialized)
  $perlwarn = $^W;
  $^W = 0;
	
  # Get several useful env variables
  $type = $ENV{'CONTENT_TYPE'};
  $len  = $ENV{'CONTENT_LENGTH'};
  $meth = $ENV{'REQUEST_METHOD'};
  
  if ($len > $cgi_lib'maxdata) { #'
      &CgiDie("cgi-lib.pl: Request to receive too much data: $len bytes\n");
  }
  
  if (!defined $meth || $meth eq '' || $meth eq 'GET' || 
      $type eq 'application/x-www-form-urlencoded') {
    local ($key, $val, $i);
	
    # Read in text
    if (!defined $meth || $meth eq '') {
      $in = $ENV{'QUERY_STRING'};
      $cmdflag = 1;  # also use command-line options
    } elsif($meth eq 'GET' || $meth eq 'HEAD') {
      $in = $ENV{'QUERY_STRING'};
    } elsif ($meth eq 'POST') {
        $errflag = (read(STDIN, $in, $len) != $len);
    } else {
      &CgiDie("cgi-lib.pl: Unknown request method: $meth\n");
    }

    @in = split(/[&;]/,$in); 
    push(@in, @ARGV) if $cmdflag; # add command-line parameters

    foreach $i (0 .. $#in) {
      # Convert plus to space
      $in[$i] =~ s/\+/ /g;

      # Split into key and value.  
      ($key, $val) = split(/=/,$in[$i],2); # splits on the first =.

      # Convert %XX from hex numbers to alphanumeric
      $key =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;
      $val =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;

      #Remove all HTML tags
      $val =~ s/<([^>]|\n)*>//g;

      # Associate key and value
      $in{$key} .= "\0" if (defined($in{$key})); # \0 is the multiple separator
      $in{$key} .= $val;
    }

  } elsif ($ENV{'CONTENT_TYPE'} =~ m#^multipart/form-data#) {
    # for efficiency, compile multipart code only if needed
$errflag = !(eval <<'END_MULTIPART');

    local ($buf, $boundary, $head, @heads, $cd, $ct, $fname, $ctype, $blen);
    local ($bpos, $lpos, $left, $amt, $fn, $ser);
    local ($bufsize, $maxbound, $writefiles) = 
      ($cgi_lib'bufsize, $cgi_lib'maxbound, $cgi_lib'writefiles);


    # The following lines exist solely to eliminate spurious warning messages
    $buf = ''; 

    ($boundary) = $type =~ /boundary="([^"]+)"/; #";   # find boundary
    ($boundary) = $type =~ /boundary=(\S+)/ unless $boundary;
    &CgiDie ("Boundary not provided") unless $boundary;
    $boundary =  "--" . $boundary;
    $blen = length ($boundary);

    if ($ENV{'REQUEST_METHOD'} ne 'POST') {
      &CgiDie("Invalid request method for  multipart/form-data: $meth\n");
    }

    if ($writefiles) {
      local($me);
      stat ($writefiles);
      $writefiles = "/tmp" unless  -d _ && -r _ && -w _;
      # ($me) = $0 =~ m#([^/]*)$#;
      $writefiles .= "/$cgi_lib'filepre"; 
    }

    # read in the data and split into parts:
    # put headers in @in and data in %in
    # General algorithm:
    #   There are two dividers: the border and the '\r\n\r\n' between
    # header and body.  Iterate between searching for these
    #   Retain a buffer of size(bufsize+maxbound); the latter part is
    # to ensure that dividers don't get lost by wrapping between two bufs
    #   Look for a divider in the current batch.  If not found, then
    # save all of bufsize, move the maxbound extra buffer to the front of
    # the buffer, and read in a new bufsize bytes.  If a divider is found,
    # save everything up to the divider.  Then empty the buffer of everything
    # up to the end of the divider.  Refill buffer to bufsize+maxbound
    #   Note slightly odd organization.  Code before BODY: really goes with
    # code following HEAD:, but is put first to 'pre-fill' buffers.  BODY:
    # is placed before HEAD: because we first need to discard any 'preface,'
    # which would be analagous to a body without a preceeding head.

    $left = $len;
   PART: # find each part of the multi-part while reading data
    while (1) {
      last PART if $errflag;

      $amt = ($left > $bufsize+$maxbound-length($buf) 
	      ?  $bufsize+$maxbound-length($buf): $left);
      $errflag = (read(STDIN, $buf, $amt, length($buf)) != $amt);
      $left -= $amt;

      $in{$name} .= "\0" if defined $in{$name}; 
      $in{$name} .= $fn if $fn;

      $name=~/([-\w]+)/;  # This allows $insfn{$name} to be untainted
      if (defined $1) {
        $insfn{$1} .= "\0" if defined $insfn{$1}; 
        $insfn{$1} .= $fn if $fn;
      }
 
     BODY: 
      while (($bpos = index($buf, $boundary)) == -1) {
        if ($name) {  # if no $name, then it's the prologue -- discard
          if ($fn) { print FILE substr($buf, 0, $bufsize); }
          else     { $in{$name} .= substr($buf, 0, $bufsize); }
        }
        $buf = substr($buf, $bufsize);
        $amt = ($left > $bufsize ? $bufsize : $left); #$maxbound==length($buf);
        $errflag = (read(STDIN, $buf, $amt, $maxbound) != $amt);  
        $left -= $amt;
      }
      if (defined $name) {  # if no $name, then it's the prologue -- discard
        if ($fn) { print FILE substr($buf, 0, $bpos-2); }
        else     { $in {$name} .= substr($buf, 0, $bpos-2); } # kill last \r\n
      }
      close (FILE);
      last PART if substr($buf, $bpos + $blen, 4) eq "--\r\n";
      substr($buf, 0, $bpos+$blen+2) = '';
      $amt = ($left > $bufsize+$maxbound-length($buf) 
	      ? $bufsize+$maxbound-length($buf) : $left);
      $errflag = (read(STDIN, $buf, $amt, length($buf)) != $amt);
      $left -= $amt;


      undef $head;  undef $fn;
     HEAD:
      while (($lpos = index($buf, "\r\n\r\n")) == -1) { 
        $head .= substr($buf, 0, $bufsize);
        $buf = substr($buf, $bufsize);
        $amt = ($left > $bufsize ? $bufsize : $left); #$maxbound==length($buf);
        $errflag = (read(STDIN, $buf, $amt, $maxbound) != $amt);  
        $left -= $amt;
      }
      $head .= substr($buf, 0, $lpos+2);
      push (@in, $head);
      @heads = split("\r\n", $head);
      ($cd) = grep (/^\s*Content-Disposition:/i, @heads);
      ($ct) = grep (/^\s*Content-Type:/i, @heads);

      ($name) = $cd =~ /\bname="([^"]+)"/i; #"; 
      ($name) = $cd =~ /\bname=([^\s:;]+)/i unless defined $name;  

      ($fname) = $cd =~ /\bfilename="([^"]*)"/i; #"; # filename can be null-str
      ($fname) = $cd =~ /\bfilename=([^\s:;]+)/i unless defined $fname;
      $incfn{$name} .= (defined $in{$name} ? "\0" : "") . $fname;

      ($ctype) = $ct =~ /^\s*Content-type:\s*"([^"]+)"/i;  #";
      ($ctype) = $ct =~ /^\s*Content-Type:\s*([^\s:;]+)/i unless defined $ctype;
      $inct{$name} .= (defined $in{$name} ? "\0" : "") . $ctype;

      if ($writefiles && defined $fname) {
        $ser++;
	$fn = $writefiles . ".$$.$ser";
	open (FILE, ">$fn") || &CgiDie("Couldn't open $fn\n");
      }
      substr($buf, 0, $lpos+4) = '';
      undef $fname;
      undef $ctype;
    }

1;
END_MULTIPART
  &CgiDie($@) if $errflag;
  } else {
    &CgiDie("cgi-lib.pl: Unknown Content-type: $ENV{'CONTENT_TYPE'}\n");
  }


  $^W = $perlwarn;

  return ($errflag ? undef :  scalar(@in)); 
}


# PrintHeader
# Returns the magic line which tells WWW that we're an HTML document

sub PrintHeader {
  return "Content-type: text/html\n\n";
}


# HtmlTop
# Returns the <head> of a document and the beginning of the body
# with the title and a body <h1> header as specified by the parameter

sub HtmlTop
{
  local ($title) = @_;

  return <<END_OF_TEXT;
<html>
<head>
<title>$title</title>
</head>
<body>
<h1>$title</h1>
END_OF_TEXT
}


# HtmlBot
# Returns the </body>, </html> codes for the bottom of every HTML page

sub HtmlBot
{
  return "</body>\n</html>\n";
}


# SplitParam
# Splits a multi-valued parameter into a list of the constituent parameters

sub SplitParam
{
  local ($param) = @_;
  local (@params) = split ("\0", $param);
  return (wantarray ? @params : $params[0]);
}


# MethGet
# Return true if this cgi call was using the GET request, false otherwise

sub MethGet {
  return (defined $ENV{'REQUEST_METHOD'} && $ENV{'REQUEST_METHOD'} eq "GET");
}


# MethPost
# Return true if this cgi call was using the POST request, false otherwise

sub MethPost {
  return (defined $ENV{'REQUEST_METHOD'} && $ENV{'REQUEST_METHOD'} eq "POST");
}


# MyBaseUrl
# Returns the base URL to the script (i.e., no extra path or query string)
sub MyBaseUrl {
  local ($ret, $perlwarn);
  $perlwarn = $^W; $^W = 0;
  $ret = 'http://' . $ENV{'SERVER_NAME'} .  
         ($ENV{'SERVER_PORT'} != 80 ? ":$ENV{'SERVER_PORT'}" : '') .
         $ENV{'SCRIPT_NAME'};
  $^W = $perlwarn;
  return $ret;
}


# MyFullUrl
# Returns the full URL to the script (i.e., with extra path or query string)
sub MyFullUrl {
  local ($ret, $perlwarn);
  $perlwarn = $^W; $^W = 0;
  $ret = 'http://' . $ENV{'SERVER_NAME'} .  
         ($ENV{'SERVER_PORT'} != 80 ? ":$ENV{'SERVER_PORT'}" : '') .
         $ENV{'SCRIPT_NAME'} . $ENV{'PATH_INFO'} .
         (length ($ENV{'QUERY_STRING'}) ? "?$ENV{'QUERY_STRING'}" : '');
  $^W = $perlwarn;
  return $ret;
}


# MyURL
# Returns the base URL to the script (i.e., no extra path or query string)
# This is obsolete and will be removed in later versions
sub MyURL  {
  return &MyBaseUrl;
}


# CgiError
# Prints out an error message which which containes appropriate headers,
# markup, etcetera.
# Parameters:
#  If no parameters, gives a generic error message
#  Otherwise, the first parameter will be the title and the rest will 
#  be given as different paragraphs of the body

sub CgiError {
  local (@msg) = @_;
  local ($i,$name);

  if (!@msg) {
    $name = &MyFullUrl;
    @msg = ("Error: script $name encountered fatal error\n");
  };

  if (!$cgi_lib'headerout) { #')
    print &PrintHeader;	
    print "<html>\n<head>\n<title>$msg[0]</title>\n</head>\n<body>\n";
  }
  print "<h1>$msg[0]</h1>\n";
  foreach $i (1 .. $#msg) {
    print "<p>$msg[$i]</p>\n";
  }

  $cgi_lib'headerout++;
}


# CgiDie
# Identical to CgiError, but also quits with the passed error message.

sub CgiDie {
  local (@msg) = @_;
  &CgiError (@msg);
  die @msg;
}


# PrintVariables
# Nicely formats variables.  Three calling options:
# A non-null associative array - prints the items in that array
# A type-glob - prints the items in the associated assoc array
# nothing - defaults to use %in
# Typical use: &PrintVariables()

sub PrintVariables {
  local (*in) = @_ if @_ == 1;
  local (%in) = @_ if @_ > 1;
  local ($out, $key, $output);

  $output =  "\n<dl compact>\n";
  foreach $key (sort keys(%in)) {
    foreach (split("\0", $in{$key})) {
      ($out = $_) =~ s/\n/<br>\n/g;
      $output .=  "<dt><b>$key</b>\n <dd>:<i>$out</i>:<br>\n";
    }
  }
  $output .=  "</dl>\n";

  return $output;
}

# PrintEnv
# Nicely formats all environment variables and returns HTML string
sub PrintEnv {
  &PrintVariables(*ENV);
}


# The following lines exist only to avoid warning messages
$cgi_lib'writefiles =  $cgi_lib'writefiles;
$cgi_lib'bufsize    =  $cgi_lib'bufsize ;
$cgi_lib'maxbound   =  $cgi_lib'maxbound;
$cgi_lib'version    =  $cgi_lib'version;

1; #return true 

sub absolute {
local $url = $_[0];
$url =~ s/\n\n/\n/;
$url =~ s/^([^(http:\/\/)])/http:\/\/$1/;
local $baseurl = $url;
$baseurl =~ s/(\/[\w-]*\.\w*html*)$/\//i;
$baseurl =~ s/(\/*)$/\//;
local $basedomain = $baseurl;
$basedomain =~ s/(\.\w*\/)//i;
$basedomain = "$`$1";

local $return="";
local $html = get($url);

if ($html=~/(url=)|(The document has moved <A HREF=")/i) {
  $html=~/((url=)|(The document has moved <A HREF="))(.*)"/i;
  $newurl = $4;
  if ($newurl!~/^(http)/i) {
    $newurl =~ s/^(\/)/$basedomain/;
    $newurl =~ s/^([^(\/)])/$baseurl$1/;
  }
  $html = get($newurl);
}

@html = split(/(<!--.*?-->)|(<.*?>)/s,$html);
foreach $line (@html) {
  if ($line && ($line ne "")) {
  $_ = $line;
  if ((/(src=)|(href=)|(background=)/i) && !(/="http/i)) {
   $line =~ s/((src)|(href)|(background))=".\//$1="/i;
   $line =~ s/((src)|(href)|(background))="([^(\/)])/$1="$baseurl$5/i;
   $line =~ s/((src)|(href)|(background))="\//$1="$basedomain/i;
  }
  @return = (@return,$line);
  }
}
@return;
}
