/**
 * Helper script to create event-metadata.json template
 * 
 * This is a Node.js script to help you quickly generate event-metadata.json files
 * for your Google Drive event folders.
 * 
 * USAGE:
 * 1. Install Node.js if not already installed
 * 2. Run: node create-event-metadata-template.js
 * 3. Answer the prompts
 * 4. The script will generate event-metadata.json
 * 5. Upload the file to your event folder in Google Drive
 */

const readline = require('readline');
const fs = require('fs');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function ask(question) {
    return new Promise(resolve => {
        rl.question(question, answer => {
            resolve(answer.trim());
        });
    });
}

async function main() {
    console.log('\n=== Event Metadata Generator ===\n');
    console.log('This will help you create an event-metadata.json file.\n');
    console.log('Press Enter to skip optional fields.\n');

    const metadata = {};

    // Required fields
    metadata.date = await ask('Event date (YYYY-MM-DD): ');
    metadata.name = await ask('Event name: ');
    metadata.place = await ask('Event location: ');

    // Event type
    console.log('\nEvent types: Protest, Conference, Meeting, Vigil, Campaign, Action');
    const type = await ask('Event type (press Enter to auto-detect): ');
    if (type) metadata.type = type;

    // Organizers
    console.log('\n--- Organizers ---');
    metadata.organizers = [];
    let addMore = true;
    while (addMore) {
        const orgName = await ask(`Organizer ${metadata.organizers.length + 1} name (or press Enter to finish): `);
        if (!orgName) {
            addMore = false;
            break;
        }

        const org = { name: orgName };

        const website = await ask('  Website URL (optional): ');
        if (website) org.website = website;

        const role = await ask('  Role (e.g., Lead Organizer, Co-Organizer, Partner): ');
        if (role) org.role = role;

        metadata.organizers.push(org);
    }

    // Tags
    console.log('\n--- Tags ---');
    const tagsInput = await ask('Tags (comma-separated, e.g., Belgium, Ukraine, Sanctions): ');
    if (tagsInput) {
        metadata.tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);
    }

    // Announcement
    console.log('\n--- Event Announcement ---');
    const announcementUrl = await ask('Announcement URL (optional): ');
    if (announcementUrl) {
        metadata.announcement = { url: announcementUrl };
        const announcementTitle = await ask('Announcement title (optional): ');
        if (announcementTitle) metadata.announcement.title = announcementTitle;
        const announcementDate = await ask('Announcement date (YYYY-MM-DD, optional): ');
        if (announcementDate) metadata.announcement.date = announcementDate;
    }

    // Description
    console.log('\n--- Description ---');
    const description = await ask('Event description (optional): ');
    if (description) metadata.description = description;

    // Attendance
    console.log('\n--- Attendance ---');
    const attendanceEst = await ask('Estimated attendance (optional): ');
    if (attendanceEst) {
        metadata.attendance = { estimated: parseInt(attendanceEst) };
        const attendanceConf = await ask('Confirmed attendance (optional): ');
        if (attendanceConf) metadata.attendance.confirmed = parseInt(attendanceConf);
    }

    // Social media
    console.log('\n--- Social Media ---');
    const hashtags = await ask('Hashtags (comma-separated, optional): ');
    if (hashtags) {
        metadata.social = { hashtags: hashtags.split(',').map(t => t.trim()).filter(t => t) };

        const facebook = await ask('Facebook event URL (optional): ');
        if (facebook) metadata.social.facebook = facebook;

        const twitter = await ask('Twitter/X URL (optional): ');
        if (twitter) metadata.social.twitter = twitter;

        const instagram = await ask('Instagram URL (optional): ');
        if (instagram) metadata.social.instagram = instagram;
    }

    // Notes
    console.log('\n--- Additional Notes ---');
    const notes = await ask('Any additional notes (optional): ');
    if (notes) metadata.notes = notes;

    // Generate JSON
    const json = JSON.stringify(metadata, null, 2);
    const filename = 'event-metadata.json';

    console.log('\n=== Generated JSON ===\n');
    console.log(json);
    console.log('\n===================\n');

    const save = await ask(`Save to ${filename}? (y/n): `);
    if (save.toLowerCase() === 'y') {
        fs.writeFileSync(filename, json, 'utf8');
        console.log(`\n✅ Saved to ${filename}`);
        console.log('\nNext steps:');
        console.log('1. Review the JSON file');
        console.log('2. Upload it to your event folder in Google Drive');
        console.log('3. The file should be in the root of the event folder');
        console.log('4. Refresh your events page to see the updated information\n');
    }

    rl.close();
}

main().catch(err => {
    console.error('Error:', err);
    rl.close();
    process.exit(1);
});
