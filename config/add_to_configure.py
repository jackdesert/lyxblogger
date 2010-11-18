'''This file contains the code that I will upload to the server so that
LyxBlogger is automatically detected by LyX if it is installed.

INSTRUCTIONS
Simply change this file as desired, paste it into lyx/lib/configure.py
Right after elyxer and whetever else is in elyxer's ELSE statement

Then run lyx/lib/configure.py to make sure it compiles. If it runs with
no errors, open lyx/lyxrc.defaults to make sure the code is formatted
properly to be cleanly readable.

Append four lines added to lyx/lyxrc.defaults to ~/.lyxSUFFIX/lyxrc.dist.
Now run lyxSUFFIX to make sure your entries show up in Edit-> Export.
Make sure the options work.

As a final step, recompile lyx using the new configure.py (use the
--with-version-suffix option to make sure you have a perfectly clean
installation that doesn't share its ~/.lyxSUFFIX folder with any other
lyx installation. Run the newly compiled lyx and make sure the options
are available in LyX.

Make sure that if you remove lyxblogger and recompile, the LyxBlogger
export option goes away. make sure that if you uninstall elyxer.py the
LyxBlogger (eLyXer) export option goes away.



Material to add to messages:
El sistema ha sido reconfigurado.
Necesita reiniciar LyX para hacer uso de cualquier
especificación de clase de documento actualizada.

add to this:
Please restart LyX to see newly installed converters.


Shoulld the extension be blog or xblog, eblog or xml-rpc
Should the format name be

  LyxBlogger (LyXHTML)             LyxBlogger (eLyXer)

  LyxBlogger via LyXHTML           LyxBlogger via eLyXer

  Blog (LyxBlogger, LyXHTML)       Blog (LyxBlogger, eLyXer)

  WordPress (LyXHTML)              WordPress (eLyXer)

  WordPress (LyxBlogger, LyXHTML)  WordPress (LyxBlogger, eLyXer)






  WordPress Blog (
  WordPress (LyXHTML, LyxBlogger)

# Note this formatting has tabs only two deep.
# If your editor uses four spaces per tab, please use spaces
# manually instead of CTRL I / CTRL U / TAB to get indentation.
'''


# Test Cases
'''
TEST CASES
lib/configure.py will write the following lines to lyxrc.defaults based
on which programs are found on the machine.

A. Lyxblogger not installed
    ( no entry )

B. LyxBlogger installed
    \Format    blog       blog       "LyXBlogger"           "" "" ""  "document"
    \converter xhtml      blog       "python -m lyxblogger $$i"       ""






'''

# Trying it Out
'''
To make sure the entries work, copy the four full entries to lyxrc.dist
and reconfigure and restart lyx. Note that this test does not check whether
lyxblogger is installed-- it just takes your word for it.
'''
##################   VERBOSE COMMENTS ##################################
# Format Name: LyxBlogger
# Format Short Name: blog
#
# LyxBlogger: If LyxBlogger is installed add as a format and as a
# converter from LyXHTML to LyxBlogger. If eLyXer is also installed,
# add an additional converter from eLyXer to LyxBlogger

###################### TERSE COMMENTS INLINE WITH CODE #################

# T R U N K -- Modular version only

    # Check if LyXBlogger is installed
    lyxblogger_found = checkModule('lyxblogger')
    if lyxblogger_found:
      addToRC(r'\Format    blog       blog       "LyXBlogger"           "" "" ""  "document"')
      addToRC(r'\converter xhtml      blog       "python -m lyxblogger $$i"       ""')




# B R A N C H
# With support for .py extension

    # Check if LyxBlogger is installed (Depends on eLyXer)
    if elyxerfound:
      lyxblogger_found = checkModule('lyxblogger')
      if lyxblogger_found:
        addToRC(r'\Format    blog       blog       "LyXBlogger"           "" "" ""  "document"')
        addToRC(r'\converter html       blog       "python -m lyxblogger $$i"       ""')






'''Add the code right before the following line in lyx/lib/configure.py:

# On SuSE the scripts have a .sh suffix, and on debian they are in /usr/share/tex4ht/

Note the blank line above the # On SuSE line.'''



############################# END LYXBLOGGER ###########################
