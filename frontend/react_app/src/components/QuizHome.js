import React, { useState, useEffect } from "react";
import Home from "./Home";
import Quiz from './Questions/Quiz';
import StyleQuiz from './Questions/StyleQuiz';
import Result from './Result';

import { Typography, AppBar, Button, Card, CardActions, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container } from '@material-ui/core';

import quizQuestions from './Questions/api/quizQuestions';
import PHOTOS from './Questions/api/photos';
import QUIZPHOTOS from './Questions/api/quizPhotos';
import * as settings from "../settings";
import axios from "axios";

import useStyles from "../styles";


import ScopedCssBaseline from '@material-ui/core/ScopedCssBaseline';

import Masonry from "react-masonry-component";
// Masory Options
const masonryOptions = {
  fitWidth: false,
  columnWidth: 300,
  gutter: 30,
  itemSelector: ".photo-item",
};


function QuizHome(props) {
    const classes = useStyles();

    const [counter, setCounter] = useState(5)
    const [counterEnd, setCounterEnd] = useState(9)
    const [questionId, setQuestionId] = useState(0)
    const [question, setQuestion] = useState(quizQuestions[0].question)
    const [answer, setAnswer] = useState('')
    const [answersCount, setAnswersCount] = useState({})
    const [result, setResult] = useState('')
    const [check, setCheck] = useState(false)

    const [answerList, setAnswerList] = useState([])
    // const answerList = []
    const [styles, setStyles] = useState('')

    const shuffledAnswerOptions = quizQuestions.map((question) => shuffleArray(question.answers));
    const [answerOptions, setAnswerOptions] = useState(shuffledAnswerOptions[0])

    const shuffledPhotos = PHOTOS.map((question) => shuffleArray(PHOTOS));
    const [PhotoList, setPhotoList] = useState(
            PHOTOS.slice(0,4))

    const [prediction, setPrediction] = React.useState(null)


    const db = "./Questions/assets/subset/subset/";



    // function to shuffle answers
    function shuffleArray(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;

      // While there remain elements to shuffle...
      while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }

      return array;
    };

    function setNextQuestion() {
        const counter1 = counter + 4;
        const counter2 = counterEnd + 4;
        const questionId1 = questionId+1;
        setCounter(counter1);
        setCounterEnd(counter2);
        setQuestionId(questionId1);
        // setQuestion(quizQuestions[counter1].question);
        // setAnswerOptions(quizQuestions[counter1].answers);
        setPhotoList(PHOTOS.slice(counter1,counter2));
        setAnswer('');
    }

    function handleAnswerSelected(event) {
      // setUserAnswer(event.currentTarget.value);
      // setUserAnswer(event)
      setUserAnswer(event)
      if (questionId < 4) {
          setTimeout(() => setNextQuestion(), 300);
        } else {
          setStyles(answerList)
          // setTimeout(() => setResults(getResults()), 300);
          // setTimeout(() => setResults(answerList), 300);
          // do nothing for now
        }
    };

    // useEffect(async() => {
    //     function handlePredict(_callback) {
    //     //Axios variables required to call the predict API
    //     // let headers = { 'Authorization': `Token ${props.token}` };
    //     let url = settings.API_SERVER + '/api/recommend/';
    //     // alert(url)
    //     // let url = 'http://127.0.0.1:8000/api/recommend/';
    //
    //     let method = 'post';
    //     let config = { method, url, data: answerList };
    //     // alert(JSON.stringify(config))
    //
    //     //Axios predict API call
    //     axios(config).then(
    //         res => {
    //             //
    //             // alert(JSON.stringify(res.data["Results"]));
    //             // const x = res.data["Results"].map(item => {
    //             //     return require(item)
    //             // });
    //             setPrediction(res.data["Results"]);
    //         }).catch(
    //             error => {alert(error)})
    //      _callback();
    //     }
    // }, []);
     function handlePredict(_callback) {
        //Axios variables required to call the predict API
        // let headers = { 'Authorization': `Token ${props.token}` };
        let url = settings.API_SERVER + '/api/recommend/';
        // alert(url)
        // let url = 'http://127.0.0.1:8000/api/recommend/';
        let method = 'post';
        let config = { method, url, data: answerList };
        // alert(JSON.stringify(config))

        //Axios predict API call
        axios(config).then(
            res => {
                setPrediction(res.data["Results"]);
            }).catch(
                error => {alert(error)})
         _callback();
    }



    function checkRes() {

    }

    function setUserAnswer(answer) {
        if (answer != '') {
            setAnswersCount(
                {
                    ...answersCount,
                    [answer]: (answersCount[answer] || 0) + 1
                });
            setAnswer(answer);

            answerList.push(answer)
            setAnswerList(answerList)
        }
    }

    function getResults() {
        const answersCountKeys = Object.keys(answersCount);
        const answersCountValues = answersCountKeys.map(key => answersCount[key]);
        const maxAnswerCount = Math.max.apply(null, answersCountValues);
        console.log(answersCount + "answersCount")
        return answersCountKeys.filter(key => answersCount[key] === maxAnswerCount);
    }

    function setResults(result) {
        setResult(result);
        // if (result.length === 1) {
        //     setResult(result[0])
        // } else {
        //     setResult('Undetermined');
        // }
    }

    function renderQuiz() {
        return (
            <div>
                <Quiz
                answer={answer}
                answerOptions={answerOptions}
                questionId={questionId}
                question={question}
                questionTotal={quizQuestions.length}
                onAnswerSelected={handleAnswerSelected}
                />
            </div>
        );
    }
    function renderStyleQuiz() {
        return (

        <fade>
            <div>
                <StyleQuiz
                PhotoList={PhotoList}
                answer={answer}
                answerOptions={answerOptions}
                questionId={questionId}
                question={question}
                questionTotal={quizQuestions.length}
                onAnswerSelected={handleAnswerSelected}
                al = {answerList}
                />
            </div>
        </fade>
        );
    }

    function renderResult() {
        if (check == false) {

            handlePredict(function () {
                console.log('ensure done');
            })
            // }).catch(err => alert(err));
            // handlePredict();
            setCheck(true);
        }
        // await checkAPI();
        // alert(JSON.stringify(answerList))
        console.log("async await returning ")
        return <Result quizResult={"HI"} prediction={prediction} />;
    }

    return (
        <React.Fragment>
            <ScopedCssBaseline />
            <Container>
                <div>
                    {/*{renderStyleQuiz()}*/}
                    {/*{styles ? renderQuiz() : renderStyleQuiz()}*/}
                    {/*<img src={require('./Questions/assets/subset/subset/1.jpg')} />*/}
                    {styles ? renderResult() : renderStyleQuiz()}
                    {/*{var ren = getRender()}*/}

                    {/*{result ? renderResult() : renderQuiz()}*/}
                    {/*{renderQuiz()}*/}
                </div>
            </Container>
        </React.Fragment>
    )
};
export default QuizHome

