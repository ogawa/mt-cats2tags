#!/usr/bin/perl -w
#
# $Id$
# A simple tool for adding tags to each entries based on their categories
# 
# This software is provided as-is. You may use it for commercial or 
# personal use. If you distribute it, please keep this notice intact.
#
# Copyright (c) 2006,2007 Hirotaka Ogawa

use strict;
sub BEGIN {
    my $dir;
    require File::Spec;
    if (!($dir = $ENV{MT_HOME})) {
        if ($0 =~ m!(.*[/\\])!) {
            $dir = $1;
        } else {
            $dir = './';
        }
        $ENV{MT_HOME} = $dir;
    }
    unshift @INC, File::Spec->catdir($dir, 'lib');
    unshift @INC, File::Spec->catdir($dir, 'extlib');
}

$|=1;
print "Content-Type: text/html\n\n";
print <<HTML;
<html>
<head><title>mt-cats2tags</title></head>
<body>
<h1>mt-cats2tags</h1>

<pre>
HTML

use MT;
use MT::Entry;
use MT::Category;

my $mt = MT->new or die MT->errstr;
my $iter = MT::Entry->load_iter;

while (my $e = $iter->()) {
    my $cats = $e->categories;
    next unless $cats && @$cats;
    my @tags = map { $_->label } @$cats;
    $e->add_tags(@tags);
    $e->save_tags;
    print $e->id . ": " . join(', ', @tags) . "\n";
}

print <<HTML;
</pre>
<p><strong>Successfully added tags.</strong></p>
</body>
</html>
HTML
