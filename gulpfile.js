const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    const sass = require("gulp-sass")(require("sass"));
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");
    return gulp
        .src("assets/scss/styles.scss")
        .pipe(sass().on("error", sass.logError))
        .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
        .pipe(minify())
        .pipe(gulp.dest("static/css"));
};

/*

#1.  styles.scss 파일은 sass 파일이고, 모든 css 편집을 담당

#2.  package.json 내 script 코드 > css 스크립트 실행할 때 마다 gulp(gulpfile.js) 부름 

#3.  postCSS가 이해하는 두가지 플러그인 tailwindcss, autoprefixer
     postCSS는 styles.scss 내 코드들을 브라우저가 이해할 수 있는 css 코드로 바꿈 

#4.  모든 아웃풋을 minify, 코드를 짧게 만듦

#5.  위 라인의 결과를 static/css로 보냄, 브라우저에 보내는 건 static/css/styles.css

*/

exports.default = css;