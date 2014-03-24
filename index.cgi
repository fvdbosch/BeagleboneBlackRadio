#!/usr/bin/perl -w

use CGI qw(:standard);
use Data::Dumper;


$ENV{TERM} = "xterm-256color";

my $content = "";
my $title = "Beaglebone Black Radio";
my $query = CGI->new;
my $channelsList = do 'channels.config';
my $settings = do 'sdr.config';
my $menu = $query->param('menu') || 0;
my $mode = $query->param('mode') || 0;
my $channel = $query->param('channel') || 0;
my $play = $query->param('playing') || 0;
my $channels = keys %{$channelsList};
$channels--;
my $freq = $channelsList->{$channel}->{fm};
my $url = $channelsList->{$channel}->{web};
my $gain = $settings->{1}->{gain};
my $modulation = $settings->{1}->{modulation};
my $samplerate = $settings->{1}->{samplerate};
my $editChannelId;

# generates top of the GUI with the always visible menu buttons
# the active menu is highlighted
sub gen_header {
	$content .= $query->header(-expires=>'-1d');
	$content .= $query->start_html(-title=>$title,-style=>'style.css');
	$content .= $query->startform(-name=>'form',-method=>'post');
  
	$content .= hidden(-name=>'menu',-value=>$menu);
	$content .= hidden(-name=>'mode',-value=>$mode);
	$content .= hidden(-name=>'channel',-value=>$channel);
	$content .= hidden(-name=>'playing',-value=>$play);
	
	my $activeMenuListen;
	my $activeMenuManage;
	my $activeMenuConfigure;
	
	if($menu == 0){
		$activeMenuListen = "on";
		$activeMenuManage = "";
		$activeMenuConfigure = "";
	}
	elsif($menu == 1 || $menu == 2 || $menu == 3) {
		$activeMenuListen = "";
		$activeMenuManage = "on";
		$activeMenuConfigure = "";
	}
	elsif($menu == 4) {
		$activeMenuListen = "";
		$activeMenuManage = "";
		$activeMenuConfigure = "on";
	}
	else {
		$activeMenuListen = "";
		$activeMenuManage = "";
		$activeMenuConfigure = "";
	}
	
	my $button1 = $query->submit(-name=>'listen',-class=>'menu full listen '.$activeMenuListen,value=>' ');
	my $button2 = $query->submit(-name=>'manage',-class=>'menu full manage '.$activeMenuManage,value=>' ');
	my $button3 = $query->submit(-name=>'configure',-class=>'menu full configure '.$activeMenuConfigure,value=>' ');
  
	$content .= "<table id='container'>";  
	$content .= "<tr style='height: 20%;'><td style='width: 33%;'>$button1</td><td style='width: 33%;'>$button2</td><td style='width: 33%;'>$button3</td></tr>";
}

# Closes all opened tags
sub gen_footer {
	$content .= "</table></form></body></html>";
}

# Content of the first menu, providing playout controls
sub gen_listen {
	
	my $activeModeFm;
	my $activeModeMode;
	
	if($mode == 0){
		$activeModeFm = "on";
		$activeModeWeb = "";
	}
	elsif($mode == 1) {
		$activeModeFm = "";
		$activeModeWeb = "on";
	}
	else {
		$activeModeFm = "";
		$activeModeWeb = "";
	}
	
    my $button1 = $query->submit(-name=>'fm',-class=>'menu third fm '.$activeModeFm,-value=>' ');
    my $button2 = $query->submit(-name=>'web',-class=>'menu third web '.$activeModeWeb,-value=>' ');
    my $button3 = $query->submit(-name=>'previous',-class=>'menu third prev',-value=>' ');
	my $button4 = "";
    my $button4a = $query->submit(-name=>'play',-class=>'menu third play',-value=>' ');
	my $button4b = $query->submit(-name=>'stop',-class=>'menu third stop',-value=>' ');
    my $button5 = $query->submit(-name=>'next',-class=>'menu third next',-value=>' ');
    my $button6 = $query->submit(-name=>'volumeDown',-class=>'menu third voldown',-value=>' ');
    my $button7 = $query->submit(-name=>'volumeUp',-class=>'menu third volup',-value=>' ');
	
	my $info = "";
	
	if($play == 1) {
		$button4 = $button4b;
		$info = "Playing: $channelsList->{$channel}->{name} ($channel/$channels)";
		
	} else {
		$button4 = $button4a;
		$info = "Stopped";
	}
	
	$content .= "<tr><td colspan='3'><h2>$info</h2></td></tr>";
	$content .= "<tr style='height: 39px;'><td colspan='3'><div style='float: left;'><img src='img/beaglebone.jpg'/></div><div style='float: right;'><img src='img/element14.jpg'/></div></td></tr>";
    $content .= "<tr style='height: 20%;'><td style='width: 33%;text-align: left;'>$button1&nbsp;$button2</td><td style='width: 33%;'>$button3&nbsp;$button4&nbsp;$button5</td><td style='width: 33%;text-align: right;'>$button6&nbsp;$button7</td></tr>";
}

# Content of the second menu, listing the available channels and providing CRUD capabilities
sub gen_manage {
	my @manageChannelsValues;
	my %manageChannelsLabels;
	
	for(my $i = 1; $i <= $channels; $i++)  {
		push(@manageChannelsValues,$i);
		$manageChannelsLabels{$i} = $i.": ".$channelsList->{$i}->{name};
	}
	
    my $field1 = $query->popup_menu(-name => 'manageChannel',-values => \@manageChannelsValues,-labels => \%manageChannelsLabels); 
	my $button1 = $query->submit(-name=>'addChannel',-class=>'menu full add',-value=>' ');
    my $button2 = $query->submit(-name=>'editChannel',-class=>'menu full edit',-value=>' ');
    my $button3 = $query->submit(-name=>'deleteChannel',-class=>'menu full delete',-value=>' ');
	
    $content .= "<tr><td colspan='3'>$field1</td></tr>";	
	#$content .= "<tr><td colspan='3'>$field1</td></tr>";
	#$content .= "<tr><td colspan='3'>$field1</td></tr>";
	$content .= "<tr style='height: 39px;'><td colspan='3'><div style='float: left;'><img src='img/beaglebone.jpg'/></div><div style='float: right;'><img src='img/element14.jpg'/></div></td></tr>";
    $content .= "<tr style='height: 20%;'><td style='width: 33%;'>$button1</td><td style='width: 33%;'>$button2</td><td style='width: 33%;'>$button3</td></tr>";
}

# Page to add a new channel and configure its parameters
sub gen_add_channel {
	my $field1 = textfield('addChannelName',"",30,30);
	my $field2 = textfield('addChannelFreq',"",30,30);
	my $field3 = textfield('addChannelUrl',"",30,30);
    my $button1 = $query->submit(-name=>'saveAddChannel',-class=>'menu full save',-value=>' ');
    my $button2 = $query->submit(-name=>'cancelAddChannel',-class=>'menu full cancel',-value=>' ');
	
	$content .= "<tr><td colspan='3'><table id='container'>";
	$content .= "<tr><td style='text-align: right;'>Name:&nbsp;</td><td style='text-align: left;'>$field1</td></tr>";
	$content .= "<tr><td style='text-align: right;'>FM Frequency:&nbsp;</td><td style='text-align: left;'>$field2</td></tr>";
	$content .= "<tr><td style='text-align: right;'>Stream URL:&nbsp;</td><td style='text-align: left;'>$field3</td></tr>";
	$content .= "</table></td></tr>";
	$content .= "<tr style='height: 39px;'><td colspan='3'><div style='float: left;'><img src='img/beaglebone.jpg'/></div><div style='float: right;'><img src='img/element14.jpg'/></div></td></tr>";
    $content .= "<tr style='height: 20%;'><td style='width: 33%;'></td><td style='width: 33%;'>$button1</td><td style='width: 33%;'>$button2</td></tr>";
}

# Page to edit an exisitng channel and configure its parameters
sub gen_edit_channel {	
	my $field1 = textfield('editChannelName',$channelsList->{0}->{name},30,30);
	my $field2 = textfield('editChannelFreq',$channelsList->{0}->{fm},30,30);
	my $field3 = textfield('editChannelUrl',$channelsList->{0}->{web},30,30);
    my $button1 = $query->submit(-name=>'saveEditChannel',-class=>'menu full save',-value=>' ');
    my $button2 = $query->submit(-name=>'cancelEditChannel',-class=>'menu full cancel',-value=>' ');
	
	$content .= "<tr><td colspan='3'><table id='container'>";
	$content .= "<tr><td style='text-align: right; width: 30%;'>Name:&nbsp;</td><td style='text-align: left;'>$field1</td></tr>";
	$content .= "<tr><td style='text-align: right;'>FM Frequency:&nbsp;</td><td style='text-align: left;'>$field2</td></tr>";
	$content .= "<tr><td style='text-align: right;'>Stream URL:&nbsp;</td><td style='text-align: left;'>$field3</td></tr>";
	$content .= "</table></td></tr>";
	$content .= "<tr style='height: 39px;'><td colspan='3'><div style='float: left;'><img src='img/beaglebone.jpg'/></div><div style='float: right;'><img src='img/element14.jpg'/></div></td></tr>";
    $content .= "<tr style='height: 20%;'><td style='width: 33%;'></td><td style='width: 33%;'>$button1</td><td style='width: 33%;'>$button2</td></tr>";
}

# Content of the configuration page where some sdr settings can be provided for the rtl_fm command
sub gen_configure {
	# gain values retrieved from the "rtl_test" command
	my $field1 = $query->popup_menu(-name => 'gain',-values => ['automatic', '0.0', '0.9', '1.4', '2.7', '3.7', '7.7', '8.7', '12.5', '14.4', '15.7', '16.6', '19.7', '20.7', '22.9', '25.4', '28.0', '29.7', '32.8', '33.8', '36.4', '37.2', '38.6', '40.2', '42.1', '43.4', '43.9', '44.5', '48.0', '49.6'],-default => $gain); 
	# modulation values retrieved from the rtl_fm help 
	my $field2 = $query->popup_menu(-name => 'modulation',-values => ['fm','wbfm','raw','am','usb','lsb'],-default => $modulation); 
	my $field3 = textfield('samplerate',$samplerate,30,30);
    my $button1 = $query->submit(-name=>'saveConfig',-class=>'menu full save',-value=>' ');
    my $button2 = $query->submit(-name=>'cancelConfig',-class=>'menu full cancel',-value=>' ');
	
	$content .= "<tr><td colspan='3'><table id='container'>";
	$content .= "<tr><td style='text-align: right; width: 30%;'>Tuner gain:&nbsp;</td><td style='text-align: left;'>$field1</td></tr>";
	$content .= "<tr><td style='text-align: right;'>Modulation type:&nbsp;</td><td style='text-align: left;'>$field2</td></tr>";
	$content .= "<tr><td style='text-align: right;'>Sample rate:&nbsp;</td><td style='text-align: left;'>$field3</td></tr>";
	$content .= "</table></td></tr>";
	$content .= "<tr style='height: 39px;'><td colspan='3'><div style='float: left;'><img src='img/beaglebone.jpg'/></div><div style='float: right;'><img src='img/element14.jpg'/></div></td></tr>";
    $content .= "<tr style='height: 20%;'><td style='width: 33%;'></td><td style='width: 33%;'>$button1</td><td style='width: 33%;'>$button2</td></tr>";
}

sub main {
	
	# verify which menu button has been pressed and redirecmenu
	if(defined $query->param('listen')) {
		$menu = 0;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('manage')) {
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('configure')) {
		$menu = 4;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	
	#listen controls
	if(defined $query->param('fm')) {
		$mode = 0;
		$query->param(-name=>'mode',-value=>$mode);
		
		if($play == 1) {
			system('killall -9 mplayer > /dev/null 2>&1'); 
			system('nohup rtl_fm -f '.$freq.' -M '.$modulation.' -s 170k -A fast -r '.$samplerate.' -l 0 -E offset -E deemp -E dc -g '.$gain.' | aplay -r '.$samplerate.' -f S16_LE > /dev/null 2>&1 &');
		}
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('web')) {
		$mode = 1;
		$query->param(-name=>'mode',-value=>$mode);
		
		if($play == 1) {
			system('killall -9 rtl_fm > /dev/null 2>&1');
			system("nohup mplayer $url > /dev/null 2>&1 &"); 
		}
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('play')) {
		$play = 1;
		$query->param(-name=>'playing',-value=>$play);
		
		if($mode == 1) {
			system("nohup mplayer $url > /dev/null 2>&1 &");
		}
		else {
			system('nohup rtl_fm -f '.$freq.' -M '.$modulation.' -s 170k -A fast -r '.$samplerate.' -l 0 -E offset -E deemp -E dc -g '.$gain.' | aplay -r '.$samplerate.' -f S16_LE > /dev/null 2>&1 &');
		}
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('stop')) {
		$play = 0;
		$query->param(-name=>'playing',-value=>$play);
		
		system('killall -9 rtl_fm > /dev/null 2>&1');
		system('killall -9 mplayer > /dev/null 2>&1');
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('volumeDown')) {
		system('amixer set Headphone 5- > /dev/null 2>&1');
	}
	if(defined $query->param('volumeUp')) {
		system('amixer set Headphone 5+ > /dev/null 2>&1');
	}
	if(defined $query->param('previous')) {
		$channel--;

		if($channel == 0){
			$channel = $channels;
		}
		
		$query->param(-name=>'channel',-value=>$channel);
		
		$url = $channelsList->{$channel}->{web};
		
		if($play == 1) {
			if($mode == 1){
				system('killall -9 mplayer > /dev/null 2>&1');
				system("nohup mplayer $url > /dev/null 2>&1 &");
			}
			else {
				system('killall -9 rtl_fm > /dev/null 2>&1');
				system('nohup rtl_fm -f '.$freq.' -M '.$modulation.' -s 170k -A fast -r '.$samplerate.' -l 0 -E offset -E deemp -E dc -g '.$gain.' | aplay -r '.$samplerate.' -f S16_LE > /dev/null 2>&1 &');
			}
		}
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('next')) {
		$channel++;
		
		if($channel > $channels){
			$channel = 1;
		}
		
		$query->param(-name=>'channel',-value=>$channel);
		
		$url = $channelsList->{$channel}->{web};
		
		if($play == 1) {
			if($mode == 1){
				system('killall -9 mplayer > /dev/null 2>&1');
				system("nohup mplayer $url > /dev/null 2>&1 &");
			}
			else {
				system('killall -9 rtl_fm > /dev/null 2>&1');
				system('nohup rtl_fm -f '.$freq.' -M '.$modulation.' -s 170k -A fast -r '.$samplerate.' -l 0 -E offset -E deemp -E dc -g '.$gain.' | aplay -r '.$samplerate.' -f S16_LE > /dev/null 2>&1 &');
			}
		}
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	
	#manage controls
	if(defined $query->param('addChannel')) {		
		$menu = 2;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('saveAddChannel')) {
		my $channelId = $channels + 1;
		
		if(defined $channelId && $channelId > 0){
			if(defined $query->param('addChannelName') && defined $query->param('addChannelFreq') && $query->param('addChannelUrl')) {
				$channelsList->{$channelId}->{name} = $query->param('addChannelName');
				$channelsList->{$channelId}->{fm} = $query->param('addChannelFreq');
				$channelsList->{$channelId}->{web} = $query->param('addChannelUrl');
				
				open FILE, "> channels.config";
				print FILE Dumper($channelsList);
				close FILE;
			}
		} 
		
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('cancelAddChannel')) {
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('editChannel')) {
		my $editChannelId = $query->param('manageChannel') || 0;
		
		if(defined $editChannelId && $editChannelId > 0) {
			$channelsList->{0}->{name} = $channelsList->{$editChannelId}->{name};
			$channelsList->{0}->{fm} = $channelsList->{$editChannelId}->{fm};
			$channelsList->{0}->{web} = $channelsList->{$editChannelId}->{web};
			$channelsList->{0}->{id} = $editChannelId;
		
			open FILE, "> channels.config";
			print FILE Dumper($channelsList);
			close FILE;
		}
		
		$menu = 3;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('saveEditChannel')) {
		my $editChannelId = $channelsList->{0}->{id};
		
		if(defined $editChannelId && $editChannelId > 0) {
			$channelsList->{$editChannelId}->{name} = $query->param('editChannelName');
			$channelsList->{$editChannelId}->{fm} = $query->param('editChannelFreq');
			$channelsList->{$editChannelId}->{web} = $query->param('editChannelUrl');
			
			$channelsList->{0}->{name} = '';
			$channelsList->{0}->{fm} = '';
			$channelsList->{0}->{web} = '';
			$channelsList->{0}->{id} = '';
		
			open FILE, "> channels.config";
			print FILE Dumper($channelsList);
			close FILE;
		}
		
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('cancelEditChannel')) {
		$channelsList->{0}->{name} = '';
		$channelsList->{0}->{fm} = '';
		$channelsList->{0}->{web} = '';
		$channelsList->{0}->{id} = '';
		
		open FILE, "> channels.config";
		print FILE Dumper($channelsList);
		close FILE;
		
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('deleteChannel')) {
		my $deleteChannelId = $query->param('manageChannel') || 0;
		
		if(defined $deleteChannelId && $deleteChannelId > 0) {			
			delete $channelsList->{$deleteChannelId};
			
			open FILE, "> channels.config";
			print FILE Dumper($channelsList);
			close FILE;
		}
		
		$menu = 1;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	
	#configure controls
	if(defined $query->param('saveConfig')) {
		$settings->{1}->{gain} = $query->param('gain');
		$settings->{1}->{modulation} = $query->param('modulation');
		$settings->{1}->{samplerate} = $query->param('samplerate');
		
		open FILE, "> sdr.config";
		print FILE Dumper($settings);
		close FILE;
		
		$menu = 0;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}
	if(defined $query->param('cancelConfig')) {
		$menu = 0;
		return print "Status: 302 Moved\nLocation: index.cgi?menu=$menu&mode=$mode&channel=$channel&playing=$play\n\n";
	}

  
	gen_header();

	if($menu == 1) {
		gen_manage();
	} elsif ($menu == 2) {
		gen_add_channel();	
	} elsif ($menu == 3) {
		gen_edit_channel();	
	} elsif ($menu == 4) {
		gen_configure();	
	} else {
		gen_listen();
	}

	gen_footer();
  
	print $content;
}

main();