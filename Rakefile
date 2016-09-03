require 'date'
require 'pathname'

DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS = WRANGLE_DIR.join('scripts')
DIRS = {
    'fetched' => CORRAL_DIR.join('fetched'),
    'published' => DATA_DIR,
}

desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end


desc "Fetch the spreadsheet from the TDCJ and save it with today's date"
task :fetch_data do
    todaystring = Date.today.to_s
    destname = DIRS['fetched'] / "high-value-dataset-#{todaystring}.xlsx"
    sh ['python', SCRIPTS / 'fetch_spreadsheet.py', '>', destname].join(' ')
end


