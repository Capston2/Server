var gulp = require('gulp'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    autoprefixer = require('gulp-autoprefixer'),
    cssmin = require('gulp-cssmin'),
    rename = require('gulp-rename');

// watch
gulp.task('watch', function(){
  gulp.watch('../static/scss/*.scss', ['sass']);
});

// sass
gulp.task('sass', function(){
  return gulp.src(['../static/scss/*.scss'])
             .pipe(sourcemaps.init())
             .pipe(sass().on('error', sass.logError))
             .pipe(autoprefixer({
               browsers: ['last 2 versions'],
               cascade: false
             }))
             .pipe(sourcemaps.write('./'))
             .pipe(gulp.dest('../static/css'));
});

// css-min
// gulp.task('css-min', function () {
//     gulp.src('../src/css/style.css')
//         .pipe(cssmin())
//         .pipe(rename({suffix: '.min'}))
//         .pipe(gulp.dest('../src/css/'));
// });
