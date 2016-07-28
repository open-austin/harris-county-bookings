require 'net/http'
require 'date'
require 'fileutils'

module HarrisCounty
  ##
  # A module to fetch and save data from HarrisCounty::JIMS_1058_URL
  module JIMSFetcher
    ##
    # Reads the raw data from HarrisCounty::JIMS_1058_URL
    def self.read
      Net::HTTP.get(URI.parse(HarrisCounty::JIMS_1058_URL))
    end

    ##
    # Fetches and saves data from HarrisCounty::JIMS_1058_URL to a file. The name of the file is based on the given
    # date. A date of 2016-07-27 will result in a file of 2016/2016-07-27.accdb
    # TODO: Support saving as both .csv and .accdb?
    def self.save(date, directory = DATA_DIR)
      file_path = file_path date, directory
      # make sure the directories exist
      FileUtils.mkdir_p File.dirname(file_path)
      File.open(file_path, 'w') { |file| file.write read }
      file_path
    end

    def self.file_path(date, directory)
      File.join directory, date.year.to_s, "#{date.strftime('%Y-%m-%d')}.accdb"
    end
  end
end
