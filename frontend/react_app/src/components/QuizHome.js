import React, { useState } from "react";
import Home from "./Home";
import quizQuestions from './Questions/api/quizQuestions';
import Quiz from './Questions/Quiz';
import StyleQuiz from './Questions/StyleQuiz';
import Result from './Result';
import {Button, Container, Grid} from "@material-ui/core";
import CssBaseline from "@material-ui/core/CssBaseline";
import {makeStyles} from "@material-ui/core/styles";
import {Link} from "react-router-dom";


function QuizHome(props) {
// const [state, setState] = useState({
//      order:'',
//      paid: false,
//      submitting: false,
//      loading: false,
//      data: initialValues
//   });
//   // example of setting this kind of state
//   const sampleChanger = () => {
//      setState({...state, paid: true, order: 'sample'});
//   }
    // Set state for quiz
    const [counter, setCounter] = useState(0)
    const [questionId, setQuestionId] = useState(1)
    const [question, setQuestion] = useState(quizQuestions[0].question)
    const [answer, setAnswer] = useState('')
    const [answersCount, setAnswersCount] = useState({})
    const [result, setResult] = useState('')

    const [styles, setStyles] = useState('')

    // // Similar to componentDidMount and componentDidUpdate:
    // React.useEffect(() => {
    // props.setAuthenticatedIfRequired();
    // }, []);
    // Set of questions
    const shuffledAnswerOptions = quizQuestions.map((question) => shuffleArray(question.answers));
    const [answerOptions, setAnswerOptions] = useState(shuffledAnswerOptions[0])
    // const [, set] =
    // const [, set] =
    // const [, set] =
    // const [, set] =

    //
    // React.useEffect(() => {
    //
    //
    //   this.setState({
    //     question: quizQuestions[0].question,
    //     answerOptions: shuffledAnswerOptions[0]
    //   });
    //     props.setAuthenticatedIfRequired();
    // }, []);


    // // Import images regardless of file name
    // function importAll(r) {
    //   return r.keys().map(r);
    // }
    //
    // const images = importAll(require.context('./Questions/assets', false, /\.(png|jpe?g|svg)$/));
    // console.log(images);

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
        const counter1 = counter + 1;
        const questionId1 = questionId + 1;
        setCounter(counter1);
        setQuestionId(questionId1);
        setQuestion(quizQuestions[counter1].question);
        setAnswerOptions(quizQuestions[counter1].answers);
        setAnswer('');

        // this.setState({
        //   counter: counter,
        //   questionId: questionId,
        //   question: quizQuestions[counter].question,
        //   answerOptions: quizQuestions[counter].answers,
        //   answer: ''
        // });
    }


    function handleAnswerSelected(event) {
      setUserAnswer(event.currentTarget.value);

      if (questionId < quizQuestions.length) {
          setTimeout(() => setNextQuestion(), 300);
        } else {
          setTimeout(() => setResults(getResults()), 300);
          // do nothing for now
        }
    };


    function setUserAnswer(answer) {
        setAnswersCount(
            {...answersCount,
                [answer]:(answersCount[answer] || 0) + 1
                });
        setAnswer(answer);
        // this.setState((state, props) => ({
        //   answersCount: {
        //     ...state.answersCount,
        //     [answer]: (state.answersCount[answer] || 0) + 1
        //   },
        //   answer: answer
        // }));
    }

    function getResults() {
        const answersCountKeys = Object.keys(answersCount);
        const answersCountValues = answersCountKeys.map(key => answersCount[key]);
        const maxAnswerCount = Math.max.apply(null, answersCountValues);
        console.log(answersCount + "answersCount")
        return answersCountKeys.filter(key => answersCount[key] === maxAnswerCount);
    }

    function setResults(result) {
        setResult(result)
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
                {/*<Link to="/result" >*/}
                {/*    <Button variant="contained" color="primary">*/}
                {/*        See Results*/}
                {/*    </Button>*/}
                {/*</Link>*/}
            </div>
        );
    }
    function renderStyleQuiz() {
        return (
            <div>
                <StyleQuiz
                answer={answer}
                answerOptions={answerOptions}
                questionId={questionId}
                question={question}
                questionTotal={quizQuestions.length}
                onAnswerSelected={handleAnswerSelected}
                />
                {/*<Link to="/result" >*/}
                {/*    <Button variant="contained" color="primary">*/}
                {/*        See Results*/}
                {/*    </Button>*/}
                {/*</Link>*/}
            </div>
        );
    }


    function renderResult() {
        return <Result quizResult={result} />;
    }

    return (
        <React.Fragment>
            <CssBaseline />
            <Container>

                <div>
                    <h2>Design Preferences</h2>
                    {/*{renderStyleQuiz()}*/}
                    {styles ? renderQuiz() : renderStyleQuiz()}
                    {result ? renderResult() : renderQuiz()}
                    {/*{renderQuiz()}*/}
                </div>
            </Container>
        </React.Fragment>
    )
};

export default QuizHome