#include <iostream>
#include "tarjeta.hpp"
#include <string.h>
#include <iomanip>
#include "usuario.hpp"
bool luhn(const Cadena&);
using namespace std;
Numero::Numero(const Cadena& num_){
	char keys[]= "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	size_t  ii = strcspn(num_.c_str(),keys);

	if(ii<num_.length()) throw Incorrecto(Razon::DIGITOS);
				char *pch;
				char *aux = new char[30];
				pch = strpbrk (const_cast<char*>(num_.c_str()), "1234567890");
				int i = 0;
				while (pch != NULL){
						aux[i++]=*pch;
						pch = strpbrk(pch+1, "1234567890");
				}
				aux[i]='\0';
				Cadena n(aux);
				delete[] aux;

	size_t longitud = n.length();
	
	if(longitud < 13 || longitud > 19){
	throw Incorrecto (Razon::LONGITUD);
	}
	
	if(!luhn(n)){
	throw Incorrecto (Razon::NO_VALIDO);
	}

	
	numero = n;
	
}

Numero::~Numero(){}

Tarjeta::Tarjeta(const Numero& numeros, Usuario& usuario, const Fecha& fechas): numero_(numeros), usuario_(&usuario), fecha_(fechas), activa_(1), tipo_(esTipo()){
	Fecha hoy;
	if(fecha_ < hoy ){
		throw Caducada(fecha_);
	}
	usuario_ -> es_titular_de(*this);
}
Tarjeta::~Tarjeta(){
	if(usuario_ ) {
		usuario_-> no_es_titular_de(*this);
	}
}
bool operator <(const Numero& a, const Numero& b){return strcmp(a,b)<0;}
bool operator <(const Tarjeta& a, const Tarjeta& b){return a.numero() < b.numero();}
bool operator >(const Tarjeta& a, const Tarjeta& b){return b.numero() < a.numero();}
bool& Tarjeta::activa(bool a){activa_=a; return activa_;}

Tarjeta::Caducada::Caducada(const Fecha& f):fecha_caducada(f){} //Tarjeta Caducada
Tarjeta::Num_duplicado::Num_duplicado(const Numero& n):numero_(n){} //Numero duplicado
const Numero& Tarjeta::Num_duplicado::que()const{return numero_;}
Tarjeta::Desactivada::Desactivada(){} //Tarjeta desactivada

void Tarjeta::anula_titular(){
	activa_ = false;
	const_cast<Usuario*&>(usuario_) = nullptr;
}

Tarjeta::Tipo Tarjeta::esTipo(){
	int a = atoi(numero_.num().substr(0,2).c_str());
	switch(a/10){
					case 3:
							if(a==34 || a==37) return Tarjeta::AmericanExpress;
							else return Tarjeta::JCB; break;
					case 4: return Tarjeta::VISA;break;
					case 5: return Tarjeta::Mastercard;break;
					case 6: return Tarjeta::Maestro;break;
					default: return Tarjeta::Otro;
}
}
void eliminarChar(Cadena& cad, size_t post){
Cadena nuevo = cad.substr(0,post);
if((post+1)<cad.length())
	nuevo += Cadena(cad.substr(post+1,cad.length()));
cad = move(nuevo);
}
std::ostream& operator <<(std::ostream& os, const Tarjeta& t){
   
os<<t.tipo()<<std::endl<<t.numero()<<std::endl;
Cadena aux = t.titular()->nombre();
int i = 0;
while(aux[i]!='\0'){
	if(islower(aux[i])) {
		aux[i] = toupper(aux[i]);
		i++;
	}
}
os << aux << " ";
i=0;
aux=t.titular()->apellidos();

while(aux[i]!='\0'){
	if(islower(aux[i])){
		aux[i]=toupper(aux[i]);
		i++;
	}
}
os<< aux << std::endl;

os << "Caduca: " << std::setfill('0')<<std::setw(2)<<t.caducidad().mes()<<'/'<< std::setw(2)<<(t.caducidad().anno() % 100) << std::endl;
return os;
}

ostream& operator <<(ostream& os, const Tarjeta::Tipo& tipo) {
    switch(tipo) {
        case Tarjeta::VISA: os << "VISA"; break;
        case Tarjeta::Mastercard: os << "Mastercard"; break;
        case Tarjeta::Maestro: os << "Maestro"; break;
        case Tarjeta::JCB: os << "JCB"; break;
        case Tarjeta::AmericanExpress: os << "AmericanExpress"; break; 
	case Tarjeta::Otro: os <<"Otro"; break;
		default: os << "Error";
    }
    return os;
}



