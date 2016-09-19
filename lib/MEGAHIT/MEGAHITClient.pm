package MEGAHIT::MEGAHITClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

MEGAHIT::MEGAHITClient

=head1 DESCRIPTION


A KBase module to wrap the MEGAHIT package.


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => MEGAHIT::MEGAHITClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my $token = Bio::KBase::AuthToken->new(@args);
	
	if (!$token->error_message)
	{
	    $self->{token} = $token->token;
	    $self->{client}->{token} = $token->token;
	}
        else
        {
	    #
	    # All methods in this module require authentication. In this case, if we
	    # don't have a token, we can't continue.
	    #
	    die "Authentication failed: " . $token->error_message;
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 run_megahit

  $output = $obj->run_megahit($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MEGAHIT.MegaHitParams
$output is a MEGAHIT.MegaHitOutput
MegaHitParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a string
	read_library_name has a value which is a string
	output_contigset_name has a value which is a string
	megahit_parameter_preset has a value which is a string
	min_count has a value which is an int
	k_min has a value which is an int
	k_max has a value which is an int
	k_step has a value which is an int
	k_list has a value which is a reference to a list where each element is an int
	min_contig_len has a value which is an int
MegaHitOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MEGAHIT.MegaHitParams
$output is a MEGAHIT.MegaHitOutput
MegaHitParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a string
	read_library_name has a value which is a string
	output_contigset_name has a value which is a string
	megahit_parameter_preset has a value which is a string
	min_count has a value which is an int
	k_min has a value which is an int
	k_max has a value which is an int
	k_step has a value which is an int
	k_list has a value which is a reference to a list where each element is an int
	min_contig_len has a value which is an int
MegaHitOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub run_megahit
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function run_megahit (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to run_megahit:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'run_megahit');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MEGAHIT.run_megahit",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'run_megahit',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method run_megahit",
					    status_line => $self->{client}->status_line,
					    method_name => 'run_megahit',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "MEGAHIT.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "MEGAHIT.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'run_megahit',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method run_megahit",
            status_line => $self->{client}->status_line,
            method_name => 'run_megahit',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for MEGAHIT::MEGAHITClient\n";
    }
    if ($sMajor == 0) {
        warn "MEGAHIT::MEGAHITClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 MegaHitParams

=over 4



=item Description

Run MEGAHIT.  Most parameters here are just passed forward to MEGAHIT

workspace_name - the name of the workspace for input/output
read_library_name - the name of the PE read library (SE library support in the future)
output_contig_set_name - the name of the output contigset

megahit_parameter_preset - 
        override a group of parameters; possible values:
            meta            '--min-count 2 --k-list 21,41,61,81,99'
            (generic metagenomes, default)
            meta-sensitive  '--min-count 2 --k-list 21,31,41,51,61,71,81,91,99'
            (more sensitive but slower)
            meta-large      '--min-count 2 --k-list 27,37,47,57,67,77,87'
            (large & complex metagenomes, like soil)
            bulk            '--min-count 3 --k-list 31,51,71,91,99 --no-mercy'
            (experimental, standard bulk sequencing with >= 30x depth)
            single-cell     '--min-count 3 --k-list 21,33,55,77,99,121 --merge_level 20,0.96'
            (experimental, single cell data)

min_count - minimum multiplicity for filtering (k_min+1)-mers, default 2

            min_k - minimum kmer size (<= 127), must be odd number, default 21
            max_k - maximum kmer size (<= 127), must be odd number, default 99
        k_step - increment of kmer size of each iteration (<= 28), must be even number, default 10

        k_list - list of kmer size (all must be odd, in the range 15-127, increment <= 28);
 override `--k-min', `--k-max' and `--k-step'

min_contig_length - minimum length of contigs to output, default 200

@optional megahit_parameter_preset
@optional min_count
@optional k_min
@optional k_max
@optional k_step
@optional k_list
@optional min_contig_len


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a string
read_library_name has a value which is a string
output_contigset_name has a value which is a string
megahit_parameter_preset has a value which is a string
min_count has a value which is an int
k_min has a value which is an int
k_max has a value which is an int
k_step has a value which is an int
k_list has a value which is a reference to a list where each element is an int
min_contig_len has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a string
read_library_name has a value which is a string
output_contigset_name has a value which is a string
megahit_parameter_preset has a value which is a string
min_count has a value which is an int
k_min has a value which is an int
k_max has a value which is an int
k_step has a value which is an int
k_list has a value which is a reference to a list where each element is an int
min_contig_len has a value which is an int


=end text

=back



=head2 MegaHitOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=cut

package MEGAHIT::MEGAHITClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
