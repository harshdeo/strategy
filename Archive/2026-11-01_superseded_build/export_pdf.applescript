on run argv
  set inPath to POSIX file (item 1 of argv)
  set outPath to POSIX file (item 2 of argv)
  tell application "Keynote"
    set theDoc to open inPath
    export theDoc to outPath as PDF with properties {PDF image quality:Good}
    close theDoc saving no
  end tell
end run
