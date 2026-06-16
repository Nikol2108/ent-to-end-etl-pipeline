

// // 1. Count the total number of tracks in the dataset

// use('Project_ETL');

// db.getCollection("SpotifyData").countDocuments()



// // 2. Count the number of tracks grouped by album type

// use('Project_ETL');

// db.getCollection("SpotifyData").aggregate([
//     {
//         $group: {
//             _id: "$album_type",
//             Total_Tracks_By_Album_Type: { $sum: 1 }
//         }
//     }
// ])




// // 3. AVG track duration in minutes for all tracks (Without grouping by)

// use('Project_ETL');


// db.getCollection("SpotifyData").aggregate([
//     {
//         $group: {
//             _id: null,
//             Average_Track_Duration_Minutes: { $avg: { $divide: ["$track_duration_ms", 6000] } }
//         }
//     }
// ])
 



// // 4. (artist_popularity > 80 or artist_followers > 30,000,000) and track_popularity >= 75

// use('Project_ETL');

// db.getCollection("SpotifyData").find(
//     {
//         $and: [
//             {
//                 $or: [
//                     { artist_popularity: { $gt: 80 } },
//                     { artist_followers: { $gt: 30000000 } }
//                 ]
//             },
//             { track_popularity: { $gte: 75 } }
//         ]
//     },
//     {
//         artist_name: 1,
//         track_name: 1,
//         artist_popularity: 1,
//         track_popularity: 1,
//         _id: 0
//     }
// )


// // 5. Aggregation to find the maximum and minimum track popularity for each artist

// use('Project_ETL');

// db.getCollection("SpotifyData").aggregate([
//     {
//         $group: {
//             _id: "$artist_name",
//             Max_Popularity: { $max: "$track_popularity" },
//             Min_Popularity: { $min: "$track_popularity" }
//         }
//     },
//     {
//         $sort: { Max_Popularity: -1 }
//     }
// ])




// // 6. top 5 most popular tracks, projecting only relevant fields

// use('Project_ETL');

// db.getCollection('SpotifyData').aggregate([
//     {
//         $project: { 
//             _id: 0, 
//             track_name: 1, 
//             artist_name: 1, 
//             track_popularity: 1 
//         }
//     },
//     {
//         $sort: { track_popularity: -1 }
//     },
//     {
//         $limit: 5
//     }
    
// ])



// // 7. Count tracks with missing or empty track_name / album_release_date
// use('Project_ETL');

// db.getCollection("SpotifyData").countDocuments({
//     $or: [
//         { track_name: { $in: [null, "", " "] } },
//         { track_name: { $exists: false } },
//         { album_release_date: { $in: [null, ""] } },
//         { album_release_date: { $exists: false } }
//     ]
//     },
//     {
//         $project: { track_id: 1,
//                     track_name: 1,

//         }
//     }
// )


// // 8. duplicate track_id
// use('Project_ETL');

// db.getCollection("SpotifyData").aggregate([
//     {
//         $group: {
//             _id: "$track_id",
//             count: { $sum: 1 },
//             track_names: { $push: "$track_name" } 
//         }
//     },
//     {
//         $match: {
//             count: { $gt: 1 } 
//         }
//     }
// ])



// // 9. Count rows where artist_genres contains brackets or quotes (dirty data)
// use('Project_ETL');

// db.getCollection("SpotifyData").countDocuments({
//     artist_genres: { $regex: /\[|\]|'/ }
// })




// // 10. Find corrupted or incomplete release dates (saved as numbers or strings instead of Date objects)
// use('Project_ETL');

// db.getCollection("SpotifyData").countDocuments(
//     { 
//         album_release_date: { $type: ["number", "string"] } 
//     }
// )






