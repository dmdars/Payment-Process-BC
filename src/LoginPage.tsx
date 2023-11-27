import './css/LoginPage.css'

const LoginPage = () => {

	return (
		<>
			<div className="container">
				<div className="login">
					<h1> Welcome to Menta! </h1>
					<input type="email" placeholder="Username"/>
					<input type="password" placeholder="Password"/>
					<br /> <br />
					<button type='submit' className="btn btn-primary btn-block btn-large">Login</button>
				</div>
			</div>
		</>
	)
};

export default LoginPage;