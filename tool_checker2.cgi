#!c:\Perl\bin\perl

#  tool_checker2.cgi v.3.0.3 (c)2007-2014 Francisc TOTH
#  This is a module of the online radioamateur examination program
#  "SimEx Radio", created for YO6KXP ham-club located in Sacele, ROMANIA
#  All rights reserved by YO6OWN Francisc TOTH
#  Made in Romania

#ch 3.0.3 minor hardening for deregulated db
#ch 3.0.2 eliminate hamxam
#ch 3.0.1 hiding the v3code for good
#ch 3.0.0 (wrongly)hiding the v3code
#ch 0.0.f displaying deregulated databases
#ch 0.0.e s-a insensibilizat la  continutul URL-ului; Sa faca drop fara raspuns inca nu am reusit
#ch 0.0.d <title> changed to 'Probleme si Rezolvari' 
#ch 0.0.c solve tt39  colors changed so eyes can rest
#ch 0.0.b solve tt34-2, ANC renamed to ANCOM
#ch 0.0.a solve tt34, ANRCTI renamed to ANC
#ch 0.0.9 solve tt29, the part related to databases


use strict;
use warnings;


my $get_buffer; #intrarea
my $get_filename; #hamquest database filename
my $counter; #counterul 0..n al liniei unei inregistrari
my $reg; #numarul inregistrarii curente
my $rasp; #raspunsul corect al intrebarii
my $fline; #linia de fisier
my @splitter; #taietorul de v3code
sub dienice($);


$get_buffer=$ENV{'QUERY_STRING'};

if (defined($get_buffer)) {   #eliminate possibility of void input

if($get_buffer =~ m/((db_{1}(op|legis){1}(1|2|3r|3){1}){1}|(db_{1}ntsm{1}){1}|(db_{1}tech{1}(1|2|3){1}){1})/)
       {$get_filename = $1;}
       else {$get_filename = "";}

####open hamquest file
if($get_filename ne "") { #eliminate the possibility of input without filename

if(open(INFILE,"<", $get_filename)) { #open the question file


#flock(INFILE,1);		        #LOCK_SH, file can be read

seek(INFILE,0,0);			#goto begin of file

print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n!;
print qq!<title>Probleme si Rezolvari: $get_filename</title>\n!;
print qq!</head>\n!;
print qq!<body bgcolor="#E6E6FA" text="black" link="blue" alink="blue" vlink="blue">\n!;

print qq!<font color="blue">v.3.0.3</font>\n<br>\n!;

print qq!<i>Aceasta este o afisare a bazelor de date folosite de programul SimEx, un simulator de examen de radioamatori<br>Acest program este un software gratuit, poate fi distribuit/modificat in termenii licentei libere GNU GPL, asa cum este ea publicata de Free Software Foundation in versiunea 2 sau intr-o veriune ulterioara.<br>Programul, intrebarile si raspunsurile sunt distribuite gratuit, in speranta ca vor fi folositoare, dar fara nicio garantie, sau garantie implicita, vezi textul licentei GNU GPL pentru mai multe detalii.<br>In distributia programului SimEx trebuie sa gasiti o copie a licentei GNU GPL, iar daca nu, ea poate fi descarcata gratuit de pe pagina <a href="http://www.fsf.org" target="_new">http://www.fsf.org</a><br>Textul intrebarilor oficiale publicate de ANCOM face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL, modificarea lor si/sau folosirea lor in afara Romaniei in alt mod decat read-only nefiind permisa. Acest lucru deriva din faptul ca ANCOM este o institutie publica romana, iar intrebarile publicate au caracter de document oficial.</i><br>\n!;

$fline=<INFILE>;
chomp($fline);
print qq!<font color="blue">$fline</font>\n<br>\n!; #print file version



$counter = 15;
print qq!<hr>\n!;

#parcurgi fisierul
while ($fline = <INFILE>)
{
chomp($fline);				 #cut <CR> from end

if ($fline =~ m/^##[0-9]+#$/)
                        {
                        print qq!$fline\n<br>\n!;
                        $counter = 0;
			$rasp = 'f';
			}

elsif ($counter == 0)
       {
         if($fline =~ m/^[a-d]$/ )
           {
          
	   $rasp=$fline;
	   $counter = 1;
	   }

      else {$counter = 16; }
       }
    
elsif( $counter == 1)
{

if($fline =~ m/^[0-9]{2,3}[A-Z]{1}[0-9]{2,}[a-z]?~&/) 
   {
     @splitter = split(/~&/,$fline);
     print qq!$splitter[1]<br>\n!;	
   }
else {print qq!$fline<br>\n!;}

$counter = 2;
 }

elsif (( $counter == 2) || ($counter == 8))
{
 if($fline =~ m/(jpg|JPG|gif|GIF|png|PNG|null){1}/)
          {      
	my @linesplit;
	@linesplit=split(/ /,$fline);
        if(defined($linesplit[1])) 
	 	{
	 	print qq!<br><center><img src="http://localhost:8080/shelf/$linesplit[0]", width="$linesplit[1]"></center><br>\n!;
                }                     
     	  if ($counter < 3) {$counter = 3;}
       	  else {$counter = 9;}
	 }
 else {$counter = 17; }

}


elsif( $counter == 3) 
 {
     print qq!<form action="#">\n!;
if ($rasp eq 'a' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;}
        
    $counter = 4;


 if ($rasp eq 'f') { $counter =18;}

  }


elsif( $counter == 4) 
{
if ($rasp eq 'b' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;}
       $counter = 5;
}

elsif( $counter == 5) 
{
	if ($rasp eq 'c' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;}
        else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;}

       	$counter = 6;
}


elsif( $counter == 6) 
{
if ($rasp eq 'd' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;}
print qq!</form>\n<br>\n!;
       $counter = 7;
                      }


elsif($counter == 7) 
{
  print qq!<font size="-1"><i>(Contributor: $fline)</i></font><br>\n!;
  $counter = 8;
			 }


elsif($counter ==  9) 
 {
	unless ($fline eq "") {  print qq!<br>\n$fline<br>\n!;} 
	$counter = 10; 
        if ($fline =~ /^[a-d]$/) { $counter = 19; }
 }


elsif($counter ==  10) 
 {
	unless ($fline eq "") 
          { print qq!<font size="-1"><i>(rezolvare: $fline)</i></font><br>\n!;} 
            print qq!<hr>\n!;
	    $counter = 11; 

       if ($fline =~ /^[a-d]$/) { $counter = 20; }
 }

if($counter > 15) 
{
print qq!<font color="red">EROARE in baza de date, ar trebui sa anuntati adminul cod eroare: $counter</font><br><hr>\n!;
$counter = 15;
}


}

print qq!</body>\n!;
print qq!</html>\n!;

 
close (INFILE) ||die("cannot close, $!\n");

} #close file
else  {dienice($get_filename);} #else the case when correct filename could not be opened

}
else {dienice("junk input");} #else the case when input was not void, but some junk

}
else {dienice("void URL");} #else the case when URL input was void

sub dienice($)
{

print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n!;
print qq!<title>SimEx by YO6OWN</title>\n!;
print qq!</head>\n!;
print qq!<body bgcolor="forestgreen" text="white">\n!;
foreach (@_) { print "Access denied: $_"; }
print qq!</body>\n!;
print qq!</html>!;
return 0;
}
