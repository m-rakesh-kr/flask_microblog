// $(document).ready(function() {
//     const userCount = $('#more-button').data('user-count');
//     const batchSize = 3;
//
//     const userContainer = $('#user-list');
//     const hiddenUserContainer = $('#hidden-user-list');
//     const moreButton = $('#more-button');
//
//     function showMoreUsers() {
//         hiddenUserContainer.find('li').appendTo(userContainer);
//         moreButton.hide();
//     }
//
//     if (userCount > batchSize) {
//         moreButton.show();
//
//         moreButton.on('click', function() {
//             showMoreUsers();
//         });
//     }
// });
