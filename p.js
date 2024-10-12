// const express = require('express');
// const session = require('express-session');
// const Sequelize = require('sequelize');
// const passport = require('passport');
// const LinkedInStrategy = require('passport-linkedin-oauth2').Strategy;
// const { ensureLoggedIn } = require('connect-ensure-login');
// const { Op } = require('sequelize');

// const app = express();

// // Set up session middleware
// app.use(session({
//   secret: 'XCQbspbriM3Up8oG',
//   resave: false,
//   saveUninitialized: true,
// }));

// // Initialize Passport
// app.use(passport.initialize());
// app.use(passport.session());

// // Database setup
// const sequelize = new Sequelize({
//   dialect: 'sqlite',
//   storage: 'job_seekers.db',
// });

// // Define models
// const JobSeeker = sequelize.define('jobSeeker', {
//   id: {
//     type: Sequelize.STRING,
//     primaryKey: true,
//   },
//   name: Sequelize.STRING,
//   headline: Sequelize.STRING,
//   industry: Sequelize.STRING,
//   location: Sequelize.STRING,
//   skills: Sequelize.TEXT,
//   language: Sequelize.STRING,
//   email: Sequelize.STRING,
//   lastUpdated: {
//     type: Sequelize.DATE,
//     defaultValue: Sequelize.NOW,
//   },
// });

// const User = sequelize.define('user', {
//   id: {
//     type: Sequelize.STRING,
//     primaryKey: true,
//   },
//   name: Sequelize.STRING,
//   email: {
//     type: Sequelize.STRING,
//     unique: true,
//   },
//   isAdmin: {
//     type: Sequelize.BOOLEAN,
//     defaultValue: false,
//   },
// });

// // Synchronize models with the database
// sequelize.sync();

// // LinkedIn OAuth2 setup
// const CLIENT_ID = '78cz02f6ebabpy';
// const CLIENT_SECRET = 'AAkDqDY8CKp3qjQS';
// const CALLBACK_URL = 'http://localhost:5000/callback';

// passport.use(new LinkedInStrategy({
//   clientID: CLIENT_ID,
//   clientSecret: CLIENT_SECRET,
//   callbackURL: CALLBACK_URL,
//   scope: ['profile', 'email', 'openid'],
//   state: true,
// }, (accessToken, refreshToken, profile, done) => {
//   User.findOrCreate({ where: { id: profile.id }, defaults: {
//     name: profile.displayName,
//     email: profile.emails[0].value,
//   }}).then(([user]) => {
//     return done(null, user);
//   }).catch(err => {
//     console.error('Error during user creation:', err);
//     return done(err);
//   });
// }));

// passport.serializeUser((user, done) => {
//   done(null, user.id);
// });

// passport.deserializeUser((id, done) => {
//   User.findByPk(id).then(user => {
//     done(null, user);
//   }).catch(done);
// });

// // Middleware to ensure the user is authenticated
// function loginRequired(req, res, next) {
//   if (req.isAuthenticated()) {
//     return next();
//   }
//   res.redirect('/login');
// }

// // Middleware to ensure the user is an admin
// function adminRequired(req, res, next) {
//   if (req.isAuthenticated() && req.user.isAdmin) {
//     return next();
//   }
//   res.status(403).json({ error: 'Admin access required' });
// }

// // Routes
// app.get('/', (req, res) => {
//   res.send(`
//     <h1>Welcome to Job Seeker Finder</h1>
//     <a href="/auth/linkedin">Login with LinkedIn</a>
//   `);
// });

// app.get('/login', (req, res) => {
//   res.redirect('/auth/linkedin');
// });

// app.get('/auth/linkedin',
//   passport.authenticate('linkedin'));

// app.get('/callback', 
//   passport.authenticate('linkedin', { failureRedirect: '/' }),
//   (req, res) => {
//     res.redirect('/profile');
//   });

// app.get('/profile', loginRequired, (req, res) => {
//   res.send(`Hello, ${req.user.name}. <a href="/logout">Logout</a>`);
// });

// app.get('/search', loginRequired, async (req, res) => {
//   const { query, language, industry } = req.query;
//   let where = {};

//   if (query) {
//     where = {
//       ...where,
//       [Op.or]: [
//         { name: { [Op.like]: `%${query}%` } },
//         { headline: { [Op.like]: `%${query}%` } },
//       ],
//     };
//   }

//   if (language) {
//     where = { ...where, language };
//   }

//   if (industry) {
//     where = { ...where, industry: { [Op.like]: `%${industry}%` } };
//   }

//   const jobSeekers = await JobSeeker.findAll({ where });
//   res.json(jobSeekers);
// });

// app.get('/admin/users', adminRequired, async (req, res) => {
//   const users = await User.findAll();
//   res.json(users);
// });

// app.post('/admin/make_admin/:userId', adminRequired, async (req, res) => {
//   const { userId } = req.params;
//   const user = await User.findByPk(userId);
//   if (user) {
//     user.isAdmin = true;
//     await user.save();
//     res.json({ message: `User ${user.name} is now an admin` });
//   } else {
//     res.status(404).json({ error: 'User not found' });
//   }
// });

// app.get('/logout', (req, res) => {
//   req.logout(() => {
//     res.redirect('/');
//   });
// });

// const PORT = process.env.PORT || 5000;
// app.listen(PORT, () => {
//   console.log(`Server is running on http://localhost:${PORT}`);
// });


const { Builder, By, Key, until } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio'); // You'll need to install this: npm install cheerio
const os = require('os');

async function linkedinAutomation() {
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // Login process
        await driver.get('https://www.linkedin.com/');
        await driver.findElement(By.css('[data-test-id="home-hero-sign-in-cta"]')).click();
        await driver.findElement(By.css('input[name="session_key"]')).sendKeys('houdachezaki@gmail.com', Key.TAB);
        await driver.findElement(By.css('input[name="session_password"]')).sendKeys('Astrogate2024');
        await driver.findElement(By.css('button[type="submit"]')).click();

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        await sleep(35000); // wait for 3 seconds (3000 ms)

        // await driver.findElement(By.css('#home_children_button')).click();

        
        // // await driver.findElement(By.css('[data-test-id="home-hero-sign-in-cta"]')).click();
        // await driver.findElement(By.css('input[name="session_key"]')).sendKeys('houdachezaki@gmail.com', Key.TAB);
        // await driver.findElement(By.css('input[name="session_password"]')).sendKeys('Astrogate2024');
        // await driver.findElement(By.css('button[type="submit"]')).click();

        // Define search keywords and create URL array
        let keyword = 'directeur commerciale';
        let searchUrlBase = `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(keyword)}&origin=CLUSTER_EXPANSION&sid=.lH`;
        let searchUrls = [searchUrlBase]; // Array to store search URLs

        // Function to get page content with retry logic
        async function getPageContent(url, maxRetries = 3) {
            for (let attempt = 0; attempt < maxRetries; attempt++) {
                try {
                    await driver.get(url);
                    await driver.wait(until.elementLocated(By.css('body')), 10000);
                    return await driver.getPageSource();
                } catch (error) {
                    console.error(`Attempt ${attempt + 1} failed for ${url}: ${error}`);
                    if (attempt === maxRetries - 1) throw error;
                    await driver.sleep(2000); // Wait before retrying
                }
            }
        }

        // Function to extract content using selector
        function extractContent(html, selector) {
            const $ = cheerio.load(html);
            return $(selector).html() || '';
        }

        // Create a set to store unique profile URLs
        let uniqueProfileUrls = new Set();

        for (let urlIndex = 0; urlIndex < searchUrls.length; urlIndex++) {
            let searchUrl = searchUrls[urlIndex];
            console.log(`Processing search URL: ${searchUrl}`);

            // Navigate to the search results page
            await driver.get(searchUrl);

            // Wait for profile links with increased timeout
            let profileLinks = await driver.wait(until.elementsLocated(By.css('a[href*="/in/"]')), 30000);

            for (let i = 0; i < profileLinks.length; i++) {
                try {
                    // Re-locate profile links on each iteration to avoid stale elements
                    profileLinks = await driver.findElements(By.css('a[href*="/in/"]'));
                    let profileUrl = await profileLinks[i].getAttribute('href');
                    profileUrl = profileUrl.split('?')[0]; // Clean URL

                    // Check if the URL matches the desired pattern
                    if (/^https:\/\/www\.linkedin\.com\/in\/[a-z0-9-]+$/.test(profileUrl)) {
                        uniqueProfileUrls.add(profileUrl);
                    }
                } catch (error) {
                    console.error(`Error retrieving profile URL ${i + 1}: ${error}`);
                }
            }

            // Add a delay between pages to avoid rate limiting
            await driver.sleep(3000);
        }

        // Print all unique profile URLs that match the pattern
        console.log("Unique profile URLs matching the desired pattern:");
        uniqueProfileUrls.forEach(url => console.log(url));

        // Process each unique profile URL
        for (let profileUrl of uniqueProfileUrls) {
            try {
                console.log(`Processing profile URL: ${profileUrl}`);

                // Extract profile name for file naming
                let profileName = profileUrl.split('/')[4]; // Extract profile name
                profileName = profileName.replace(/[^\w\-]/g, '_'); // Sanitize profile name

                const selector = '#profile-content > div > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.pv-profile.break-words > div > div > main > section';

                // Create temporary directory
                const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'linkedin-'));

                // Get and save temporary HTML files
                const sections = ['skills', 'education', 'experience'];
                for (let section of sections) {
                    let html = await getPageContent(profileUrl + '/details/' + section + '/');
                    fs.writeFileSync(path.join(tempDir, `${section}_temp.html`), html);
                }

                // Extract relevant parts and save permanent HTML files
                let profileData = {};
                for (let section of sections) {
                    let tempHtml = fs.readFileSync(path.join(tempDir, `${section}_temp.html`), 'utf8');
                    let relevantHtml = extractContent(tempHtml, selector);
                    fs.writeFileSync(path.join(__dirname, `${profileName}_${section}.html`), relevantHtml);
                    profileData[section] = relevantHtml;
                }

                // Function to extract structured data from HTML
                function extractStructuredData(html, section) {
                    const $ = cheerio.load(html);
                    let data = [];
                    if (section === 'skills') {
                        $('.artdeco-list__item').each((i, elem) => {
                            data.push($(elem).text().trim());
                        });
                    } else if (section === 'experience') {
                        $('.pv-entity__position-group-pager').each((i, elem) => {
                            let job = {
                                title: $(elem).find('.pv-entity__summary-info h3').text().trim(),
                                company: $(elem).find('.pv-entity__secondary-title').text().trim(),
                                duration: $(elem).find('.pv-entity__date-range span:nth-child(2)').text().trim()
                            };
                            data.push(job);
                        });
                    } else if (section === 'education') {
                        $('.pv-education-entity').each((i, elem) => {
                            let edu = {
                                school: $(elem).find('.pv-entity__school-name').text().trim(),
                                degree: $(elem).find('.pv-entity__degree-name span:nth-child(2)').text().trim(),
                                fieldOfStudy: $(elem).find('.pv-entity__fos span:nth-child(2)').text().trim(),
                                dates: $(elem).find('.pv-entity__dates span:nth-child(2)').text().trim()
                            };
                            data.push(edu);
                        });
                    }
                    return data;
                }

                // Extract structured data
                let structuredData = {};
                for (let section of sections) {
                    structuredData[section] = extractStructuredData(profileData[section], section);
                }

                // Save structured data as JSON
                let jsonFileName = path.join(__dirname, `${profileName}_structured.json`);
                fs.writeFileSync(jsonFileName, JSON.stringify(structuredData, null, 2));

                console.log(`Completed processing for ${profileName}`);

                // Remove temporary files
                for (let section of sections) {
                    fs.unlinkSync(path.join(tempDir, `${section}_temp.html`));
                }
                fs.rmdirSync(tempDir);

                // Add a delay between profiles to avoid rate limiting
                await driver.sleep(3000);
            } catch (error) {
                console.error(`Error processing profile ${profileUrl}: ${error}`);
                // Continue to the next profile if one fails
            }
        }

    } finally {
        await driver.quit();
    }
}

linkedinAutomation().catch(console.error);