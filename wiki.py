LyXBlogger allows LyX to post beautifully formatted code directly to your WordPress blog.

(:comment The directive on the line below will generate a table of content :)
(:comment (:toc:)    :)


!!Premise
LyX really is a new way of thinking about documents. There is a bit of
a learning curve about it, but once you get the formatting set up the
way you want it, each successive chapter in your book sets up exactly
the same-- automatically. It also prevents you from doing things that
don't normally make sense, like putting two spaces between a word, or
a space at the beginning of a paragraph. It won't even let you
accidentally (or on purpose) put two blank lines between paragraphs.
Content is content and layout is layout - and LyX does a good job
keeping them separate.

So many of us have become LyX addicts for these and other reasons.
But when one wants to publish to the web, as in creating an online
blog, there comes a dilemma of the ''having your cake and eating it too''
variety. Of course LyX users still want to compose everything they do
in LyX. But blogging engines, such as WordPress, don't speak LyX,
and they don't understand PDF either. They hunger for none other than
xhtml. Ah, but how to get your beautiful looking, carefully arranged
document from LyX to WordPress, while retaining your document's
organization and allowing you to still manage your own CSS style file
to tweak the formatting?

LyX die hards have done it the hard way before. Like composing a
document in LyX, then copying the screen into the blog engine
composition window, and re-adding any formatting that was lost for
titles, headings, emphasis, lists, and so on. Well those days are over.
Now you can talk directly from LyX to your favorite blogging engine.
That is, as long as your favorite blogging engine is WordPress.

!!Solution
LyXBlogger allows you to post to your WordPress blog right from
LyX. LyXBlogger 0.32 comes with the following features:

*Provides XML-RPC connectivity to WordPress Blogs
*Uploads images automatically
*Supports eLyXer XHTML format
*Supports LyX 2.0 (internal) LyXHTML format
*Extracts title from document and uses it as the posting title
*Preserves document organization hierarchy as CSS classes
*Provides consistent look among all your blog entries based on your master CSS file
*Retrieves category list from server to allow user selection
*Gives option to post to test site at blogtest.letseatalready.com
*Displays messages and gets user input through xterm window

!!Download
LyXBlogger is available as a free download from https://savannah.nongnu.org/files/?group=lyxblogger.

!!Installation
First, make sure you have Python installed on your machine. (Developed on Python 2.6.4)
Then install LyXBlogger by downloading the latest version from
[[http://code.google.com/p/lyxblogger | here]]. Install it by running
->@@$ tar -xvf LyXBlogger_x.xx.tar.gz@@
->@@$ cd LyXBlogger_x.xx/@@
->@@$ sudo cp lyxblogger /usr/bin/.@@
You must also install the wordpresslib.py library (included in LyXBlogger_x.xx.tar.gz file).
To install the wordpresslib.py library, enter the command
->@@$ python setup.py install@@
An xhtml converter is also required. Select and install an appropriate xhtml converter for
your version of LyX.
!!!Supported xhtml converters for LyX 1.6.x
*[[Tools/eLyXer]]
!!!Supported xhtml converters for LyX 2.0
*[[Tools/eLyXer]]
*LyXHTML (Internal in LyX 2.0)

!!Running
To invoke LyXBlogger, first generate (x)html by previewing LyXHTML
from LyX 2.0, or by either previewing or manually invoking eLyXer.
Then cd to the directory where the (x)html files and images reside
The location is shown in your browser window when you preview.
Invoke LyXBlogger as
->@@$ lyxblogger input_file.(x)html@@

!!!Auto Log In
LyXBlogger comes out of the box ready to upload to a test site (blogtest.letseatalready.com) where you can test its posting capability. LyXBlogger will ask you whether to post to the test site or not.
Once you can post to the test site, just run LyXBlogger again, this time telling it to use a different site instead. It will prompt you for your domain name, user name, and password.

To facilitate automatic login to your own site, just change the following lines
in the @@USER DEFINED VARIABLES@@ section of the code:
->@@AUTO_URL = [='http://blogtest.letseatalready.com/xmlrpc.php'=]@@
->@@AUTO_USER = 'test'@@
->@@AUTO_PASSWORD = 'test'@@
->@@AUTO_LOGIN = True@@
Simply put your own domain in place of blogtest.letseatalready.com, leaving the @@[=http://=]@@ and the  @@/xmlrpc.php@@ parts intact. Make sure you change @@AUTO_USER@@ to your WordPress user name and @@AUTO_PASSWORD@@ to your WordPress password. Save LyXBlogger and run it again.

!!LyX Integration
You may choose to use LyXBlogger solely from the command line. But it is often
more conventient to set up LyXBlogger as a converter inside LyX so that
you can just click a couple buttons when you are ready to upload your content.
Then LyX automatically generates the xhtml for you using your selected xhtml
converter, copies the xhtml file and any associated image files to a temporary directory,
and uses those files when invoking LyXBlogger.


!!!Converter Setup for eLyXer HTML Format
To set up LyX to use the eLyXer xhtml format when using LyXBlogger,
first install eLyXer and set it up as LyX --> HTML converter in LyX.
Use the standard options in your converter line:
->'''Converter:''' @@elyxer.py --directory $$r $$i $$o@@
For help installing eLyXer,
see  http://www.nongnu.org/elyxer/.
Next you need to find out what your eLyXer output format is called in LyX. I renamed mine
''eLyXer_HTML'' to avoid confusion.
Now go to ''Tools-> Preferences-> File Handling-> File Formats''.
Create a new file format. Give it a descriptive name like
->@@LyXBlogger Publish eLyXer_HTML to WordPress@@
Make sure you check '''Document Format'''.
Give it a unique '''Short name''' and '''Extension'''.
Then click on Converters and define a new converter as follows:
->'''From_Format:''' ''eLyXer_HTML''
->'''To_Format:''' ''LyXBlogger Publish eLyXer_HTML to WordPress''
->'''Converter:''' @@lyxblogger $$i@@
Now you can invoke this converter from within LyX by clicking ''File-> Export-> LyXBlogger Publish eLyXer_HTML to WordPress''.

!!!Converter Setup for Lyx 2.0 (internal) LyXHTML Format
LyX 2.0 comes with LyXHTML support already built in. To set up LyX to
use the internal LyXHTML format when using LyXBlogger, open LyX
2.0 and  go to ''Tools-> Preferences-> File Handling-> File Formats.''
Create a new file format. Give it a descriptive name like
->@@LyXBlogger Publish LyXHTML to WordPress@@
Make sure you check '''''Document Format'''''.
Give it a unique '''''Short name''''' and '''''Extension'''''.
Then click on '''''Converters''''' and define a new converter as follows:
->'''From_Format:''' ''LyXHTML''
->'''To_Format:''' ''LyXBlogger Publish LyXHTML to WordPress''
->'''Converter:''' @@lyxblogger $$i@@
Now you can invoke this converter from within LyX 2.0 by clicking ''File-> Export-> LyXBlogger Publish LyXHTML to WordPress''.


!!History
*'''0.32''':  Asks for confirmation before uploading to default domain. Prompts for a new title if eLyXer's default of 'Converted document' is found.
*'''0.31''':  Adds eLyXer support for LyX 1.6.x and 2.0
*'''0.30''':  Changed to xml-rpc connectivity for automated posting of xhtml and images. Runs on LyX 2.0 (internal) LyXHTML format.
*'''0.20 and previous''':  Provided copy-and-paste html output for manual posting of text only. May still be of interest for other projects.


!!Contributors
*[[mailto:jackdesert556@gmail.com|Jack Desert]]

!! Categories
(:comment Please categorize the page here :)
[[!Blog]] [[!html]] [[!xml-rpc]] [[!Publish online]]
