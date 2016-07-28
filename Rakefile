lib_dir = File.expand_path 'lib'
$LOAD_PATH.unshift(lib_dir) unless $LOAD_PATH.include?(lib_dir)

require 'harris_county_bookings'

task :save_today do
  puts HarrisCounty::JIMSFetcher.save(Date.today)
end
