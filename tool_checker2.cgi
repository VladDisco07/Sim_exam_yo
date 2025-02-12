#!/usr/bin/perl

#Prezentul simulator de examen impreuna cu formatul bazelor de intrebari, rezolvarile 
#problemelor, manual de utilizare, instalare, SRS, cod sursa si utilitarele aferente 
#constituie un pachet software gratuit care poate fi distribuit/modificat in termenii 
#licentei libere GNU GPL, asa cum este ea publicata de Free Software Foundation in 
#versiunea 2 sau intr-o versiune ulterioara. Programul, intrebarile si raspunsurile sunt 
#distribuite gratuit, in speranta ca vor fi folositoare, dar fara nicio garantie, 
#sau garantie implicita, vezi textul licentei GNU GPL pentru mai multe detalii.
#Utilizatorul programului, manualelor, codului sursa si utilitarelor are toate drepturile
#descrise in licenta publica GPL.
#In distributia de pe https://github.com/6oskarwN/Sim_exam_yo trebuie sa gasiti o copie a 
#licentei GNU GPL, de asemenea si versiunea in limba romana, iar daca nu, ea poate fi
#descarcata gratuit de pe pagina http://www.fsf.org/
#Textul intrebarilor oficiale publicate de ANCOM face exceptie de la cele de mai sus, 
#nefacand obiectul licentierii GNU GPL, copyrightul fiind al statului roman, dar 
#fiind folosibil in virtutea legii 544/2001 privind liberul acces la informatiile 
#de interes public precum al legii 109/2007 privind reutilizarea informatiilor din
#institutiile publice.

#This program together with question database formatting, solutions to problems, manuals, 
#documentation, sourcecode and utilities is a  free software; you can redistribute it 
#and/or modify it under the terms of the GNU General Public License as published by the 
#Free Software Foundation; either version 2 of the License, or any later version. This 
#program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY or
#without any implied warranty. See the GNU General Public License for more details. 
#You should have received a copy of the GNU General Public License along with this software
#distribution; if not, you can download it for free at http://www.fsf.org/ 
#Questions marked with ANCOM makes an exception of above-written, as ANCOM is a romanian
#public authority(similar to FCC in USA) so any use of the official questions, other than
#in Read-Only way, is prohibited. 

# Made in Romania

# (c) YO6OWN Francisc TOTH, 2008 - 2020

#  tool_checker2.cgi v 3.3.5 
#  Status: working
#  This is a module of the online radioamateur examination program
#  "SimEx Radio", created for YO6KXP ham-club located in Sacele, ROMANIA
#  Made in Romania

#ch 3.3.5 added possibility for adding feedback for each problem
#ch 3.3.4 charset = utf-8 added in html
#ch 3.3.3 delete d_legis2 and db_op2 from whitelist
#ch 3.3.2 strengthen whitelist
#ch 3.3.1 solving https://github.com/6oskarwN/Sim_exam_yo/issues/14 - set a max size to db_tt
#ch 3.3.0 junk input whitelist updated
#ch 3.0.5 curricula coverage sourced from strip.pl
#ch 3.0.4 minor comments changed
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
use lib '.';
use My::ExamLib qw(ins_gpl dienice);
use CGI;

my $cgi = new CGI; # variabila cgi
my $get_buffer; #intrarea
my $get_filename; #hamquest database filename
my $curricula; #associated curricula file from 1st line of database file
my $counter; #counterul 0..n al liniei unei inregistrari
my $reg; #numarul inregistrarii curente
my $rasp; #raspunsul corect al intrebarii
my $fline; #linia de fisier
my @splitter; #taietorul de v3code
my %progcodes=(); #hash of codes from curricula(keys); list of v3 codes for each chapter key
my $v3code;
my $array_size; #used to store coverage of curricula
my $buffertext;  #se va aduna aici textul intrebarii si cele 4 raspunsuri
sub dienice;


$get_buffer=$ENV{'QUERY_STRING'}; #GET

if (defined($get_buffer)) {   #eliminate possibility of void input

#we check the request to be exactly legal, to avoi sql injection or other bogus requests
if($get_buffer =~ m/^get_fname={1}((db_{1}(op|legis){1}(1|3|4){1}$){1}|(db_{1}(ntsm){1}[4]{0,1}$){1}|(db_{1}(sanctiuni){1}$){1}|(db_{1}tech{1}(1|2|3){1}$){1})/)
       {
        $get_buffer =~ m/((db_{1}(op|legis){1}(1|2|3|4){1}$){1}|(db_{1}(ntsm){1}[4]{0,1}$){1}|(db_{1}tech{1}(1|2|3){1}$){1})/;
        $get_filename=$1;
       }
       else {$get_filename = "";}

####open questions file
if($get_filename ne "") { #eliminate the possibility of input without filename

if(open(INFILE,"<", $get_filename)) { #open the question file


flock(INFILE,1);		        #LOCK_SH, file can be read

seek(INFILE,0,0);			#goto begin of db file

print $cgi -> header("text/html; charset=utf-8"); # scriere header folosind utf-8 pentru diacritice
print $cgi -> start_html("Probleme si Rezolvari: $get_filename"); # initializare html folosind titlu din argument
ins_gpl();
print qq!<font color="blue">v 3.3.5</font>\n<br>\n!;

print qq!<i>Prezentul simulator de examen împreună cu formatul bazelor de întrebări, rezolvările problemelor, manual de utilizare,<br>instalare, SRS, cod sursă și utilitarele aferente constituie un pachet software gratuit care poate fi distribuit/modificat în<br>termenii licenței libere GNU GPL, așa cum este ea publicată de Free Software Foundation în versiunea 2 sau într-o versiune <br>ulterioară. Programul, întrebările și răspunsurile sunt distribuite gratuit, în speranța că vor fi folositoare, dar fără nicio<br> garanție, sau garanție implicită, vezi textul licenței GNU GPL pentru mai multe detalii. Utilizatorul programului,<br> manualelor, codului sursă și utilitarelor are toate drepturile descrise în licența publica GPL.<br>În distribuția de pe https://github.com/6oskarwN/Sim_exam_yo trebuie să găsiți o copie a licenței GNU GPL, de asemenea <br>și versiunea în limba română, iar dacă nu, ea poate fi descărcată gratuit de pe pagina http://www.fsf.org/<br>Textul întrebărilor oficiale publicate de ANCOM face excepție de la cele de mai sus, nefăcând obiectul licențierii GNU GPL,<br> copyrightul fiind al statului român, dar fiind folosibil în virtutea legii 544/2001 privind liberul acces la informațiile <br>de interes public precum al legii 109/2007 privind reutilizarea informațiilor din instituțiile publice.</i><br>\n!;


#first line read
$fline=<INFILE>;
chomp($fline);
@splitter= split(/<\/{0,1}curricula>/,$fline);
$curricula=$splitter[1]; #we determined curricula filename


print qq!<font color="blue">$fline</font>\n<br>\n!; #print file version

#establish the v3 hash
open(PRFILE,"<", "$curricula") || print "can't open $curricula \n";
seek(PRFILE,0,0);
while($fline=<PRFILE>)
{
    if($fline =~ /^[0-9]{2,}[a-z]{0,}&/) #v3 code
     {
       @splitter = split(/&/,$fline);
       #print qq!<b>$splitter[0] </b>!; #debug
       %progcodes = (%progcodes,$splitter[0],[]); #each v3 chapter key gets reference to an array  
     }
}

#$fline=<INFILE>;       #we DO NOT read the number of records, don't fit to patterns, so it's not displayed
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
			$buffertext = "$get_filename: $fline";
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

if($fline =~ m/^[0-9]{2,3}[A-Z]{1}[0-9]{2,}[a-z]?~&/) #v3 code
   {

   @splitter = split(/~&/,$fline);
   print qq!$splitter[1]<br>\n!; #tiparim linia intrebarii cu v3 "pierdut"
   $buffertext = "$buffertext $splitter[1]";
   #putem refolosi @splitter la nevoie

   #codul v3 il bagam in hash-list daca se poate, pentru coverage
   $v3code = $splitter[0];
   @splitter = split(/[A-Z]{1}/,$v3code);
  if(defined($progcodes{$splitter[1]})) #daca exista subcapitol pt acest v3code
   {
   push(@{$progcodes{$splitter[1]}},$v3code); #add v3 to array
   #print qq!array $splitter[1]: @{$progcodes{$splitter[1]}}<br>!; #debug
   } #if defined
  } #if fline has v3 code

else {
                print qq!$fline<br>\n!; #has no v3 code, print full question
                $buffertext="$buffertext $fline";
     } 

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
	 	print qq!<br><center><img src="http://localhost/shelf/$linesplit[0]", width="$linesplit[1]"></center><br>\n!;
                }                     
     	  if ($counter < 3) {$counter = 3;}
       	  else {$counter = 9;}
	 }
 else {$counter = 17; }

}


elsif( $counter == 3) 
 { 
     print qq!<form action="#">\n!;
if ($rasp eq 'a' ) { print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;
                     #$buffertext = "$buffertext @(a)$fline";
			}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;
                     #$buffertext = "$buffertext (a)$fline";
			}
        
    $counter = 4;


 if ($rasp eq 'f') { $counter =18;} #why f???

  }


elsif( $counter == 4) 
{
if ($rasp eq 'b' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;
                     #$buffertext = "$buffertext @(b)$fline";
			}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;
                     #$buffertext = "$buffertext (b)$fline";
			}
       $counter = 5;
}

elsif( $counter == 5) 
{
	if ($rasp eq 'c' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;
                     #$buffertext = "$buffertext @(c)$fline";
			}
        else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;
                     #$buffertext = "$buffertext (c)$fline";
			}

       	$counter = 6;
}


elsif( $counter == 6) 
{

if ($rasp eq 'd' ) {print qq!<dd><input type="checkbox" value="x" name="y" checked="y" >$fline\n!;
                     #$buffertext = "$buffertext @(d)$fline";
			}
              else {print qq!<dd><input type="checkbox" value="x" name="y" disabled="y">$fline\n!;
                     #$buffertext = "$buffertext (d)$fline";
			}
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

## butonul de complaining ##
print qq!<form action="http://localhost/cgi-bin/troubleticket.cgi" method="post">\n!;
print qq!<input type="hidden" name="type" value="1">\n!;
print qq!<input type="hidden" name="nick" value="probleme_rezolvate">\n!;
print qq!<input type="hidden" name="subtxt" value=\"(propun) $buffertext\">\n!;
print qq!<font color="black" size="-1">Poți semnala ceva, poți propune o îmbunătățire, apăsând butonul </font> !;
print qq!<input type="submit" value="aici">\n!;

print qq!</form>\n!;

 
            print qq!<hr>\n!;
	    $counter = 11; 

       if ($fline =~ /^[a-d]$/) { $counter = 20; }
 }

if($counter > 15) 
{
print qq!<font color="red">EROARE în baza de date, ar trebui să anunțați adminul, cod eroare: $counter</font><br><hr>\n!;
$counter = 15;
}


}

#here we intend to print curricula coverage
print qq!<font color="blue">NOU: Afișarea acoperirii programei, pe subcapitole, cu întrebări din baza de date.</font><br><br>\n!;
print qq!<font color="blue">Valorile sunt calculate, nu completate de mână, deci fără trucuri depășite cu productivitatea la hectar.<br><br>Țineți cont că în unele cazuri, de ex. radiotehnică pentru clasa I și II la subcapitolul Legea lui Ohm și altele similare e normal să nu fie întrebări, ANCOM specifică întrebări de dificultate sporită. În alte cazuri nu sunt întrebări încă, ele nu cresc singure, trebuie făcute, așa că accept propuneri cu plăcere.</font><br>\n<br>\n!;

seek(PRFILE,0,0); #rewind curricula, we intend to print now
while($fline=<PRFILE>)
{
   if($fline =~ /^[0-9]{2,}[a-z]{0,}&/) #sub-v3 code
    {
    @splitter = split(/&/,$fline);
    $array_size = @{$progcodes{$splitter[0]}};
    print qq!<b><font color="blue">$array_size</font></b>$splitter[1]<br>!; #only counting
    }
    else  #line without sub-v3 code
    {
    print qq!$fline<br>!;
    }
}
close (PRFILE) || dienice("ERR02_cl",1,\"$! $^E $?");


print qq!</body>\n!;
print qq!</html>\n!;

close (INFILE) || dienice("ERR02_cl",1,\"$! $^E $?");

} #close file
else  {dienice("ERR01_op",1,\$get_filename);} #else the case when correct filename could not be opened

}
else {dienice("ERR01",0,\"junk input: $get_buffer");} #else the case when input was not void, but junk that fails the whitelisting

}
else {dienice("ERR01",1,\"void URL");} #else the case when URL input was void

#-------------------------------------
