const { LinkedInProfileScraper } = require('linkedin-profile-scraper');

(async () => {
  const scraper = new LinkedInProfileScraper({
    sessionCookieValue: 'AQEDARbSD4MFQ3xYAAABkfXX3BkAAAGSGeRgGU4AsDRKoznLorN7d_sE53JrVuXVHP28_E_C5oWafRq8NsInufYlmaBXfJQahNbe-vVT1rT1OzdMaoORq16DBXda_82sjhRCKV29Z_zxW0ccP8pECax0',
    keepAlive: false
  });

  await scraper.setup();

  try {
    console.log('Navigating to profile...');
    const result = await scraper.run('https://www.linkedin.com/in/zakaria-houdache/');
    console.log('Profile data:', result);
    
    // Additional debugging to inspect the result
    console.log('User Profile:', result.userProfile);
    console.log('Experiences:', result.experiences);
    console.log('Education:', result.education);
    console.log('Volunteer Experiences:', result.volunteerExperiences);
    console.log('Skills:', result.skills);
  } catch (err) {
    if (err.name === 'SessionExpired') {
      console.error('Session expired. Please update your session cookie.');
    } else {
      console.error('An error occurred:', err);
    }
  }
})();
